# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：sys.py 
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/21 15:54
"""
import datetime

from sqlalchemy.orm import relationship, backref

from poetry_fastapi.db.base_class import Base, gen_nanoid
from sqlalchemy import Column, Boolean, Integer, String, VARCHAR, Date, \
    ForeignKey
from nanoid import non_secure_generate


def get_nanoid() -> str:
    """
    生成nanoid 长度5
    """
    return non_secure_generate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", size=5)


class DictType(Base):
    code = Column(String(32), doc="字典编码")
    name = Column(String(32), doc="字典名称")
    description = Column(String(512), doc="备注")
    data = relationship("DictData", backref="type")
    __tablename__ = "dict_type"
    __table_args__ = ({'comment': '字典表'})


class DictData(Base):
    """字典明细"""
    label = Column(String(128))
    order = Column(Integer)
    remark = Column(String(512))
    type_id = Column(Integer, ForeignKey("dict_type.id", ondelete='CASCADE'))
    css_class = Column(String(128), default="", doc="css样式")
    list_class = Column(String(128), default="", doc="表格样式")
    is_default = Column(Boolean(), default=False, doc="是否默认 ")
    __tablename__ = "dict_data"
    __table_args__ = ({'comment': '字典明细'})


class Department(Base):
    """部门表"""
    code = Column(String(5), doc="部门代码")
    name = Column(String(128), doc="部门名称")
    order = Column(Integer, doc="排序")
    parent_id = Column(Integer, ForeignKey("department.id", ondelete='CASCADE'), index=True, nullable=True)
    status = Column(Boolean, doc="当前有效")
    start_date = Column(Date, default=datetime.date.today())
    end_date = Column(Date, default='3000-12-31')
    children = relationship('Department', order_by=order.asc(),
                            backref=backref('parent', uselist=False, remote_side=[id]))
    __tablename__ = "department"
    __table_args__ = ({'comment': '部门表'})


class Menu(Base):
    """ 菜单表"""
    # __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    path = Column(String(128), doc="路由")
    component = Column(String(32), doc="组件", default="")
    external_link = Column(Boolean, doc="是否外链", default=True)
    name = Column(String(32), doc="唯一标识用于页面缓存，否则keep-alive会出问题")  # index组件的name
    title = Column(String(32), doc="标题")
    icon = Column(String(32), doc="小图标")
    no_cache = Column(Boolean(), default=False, doc="是否缓存")
    affix = Column(Boolean(), default=False, doc="固钉")
    order = Column(Integer, doc="排序")
    parent_id = Column(Integer, ForeignKey("menu.id", ondelete='CASCADE'), index=True,
                       nullable=True, )  # ondelete='CASCADE' 联级删除

    parent = relationship('Menu', remote_side=[id], uselist=False, order_by=order.asc(),
                          backref=backref('children'))
    role_menu = relationship("RoleMenu", backref="menu")


###########################################

# 权限表
class Permission(Base):
    __tablename__ = "permission"
    __table_args__ = ({'comment': '权限表'})
    parent_id = Column(VARCHAR(5), default=get_nanoid, unique=True,
                       comment="所属父级权限ID")
    code = Column(VARCHAR(5), default=get_nanoid, comment="权限唯一CODE代码")
    name = Column(VARCHAR(32), comment="权限名称")
    intro = Column(VARCHAR(32), comment="权限介绍")
    category = Column(VARCHAR(32), comment="权限类别")
    uri = Column(VARCHAR(255), comment="URL规则")


# 用户账号表
# class Account(Base):
#     __tablename__ = "account"
#     user_id = Column(VARCHAR(10), ForeignKey("user.id"))  # 与用户表进行关联
#     open_code = Column(VARCHAR(255), unique=True, nullable=True,
#                        comment="登录账号，如手机号 微信号等")
#     account = Column(VARCHAR(8), default=account_nanoid, comment="账号")
#     category = Column(Integer, comment="账号类别", nullable=True)
#     __table_args__ = ({'comment': '账号表'})


# 用户组
class UserGroup(Base):
    __tablename__ = "user_group"
    parent_id = Column(VARCHAR(5), default=get_nanoid, comment="所属父级用户组ID")
    name = Column(VARCHAR(32), comment="用户组名称")
    code = Column(VARCHAR(5), default=get_nanoid, comment="用户组CODE唯一代码")
    intro = Column(VARCHAR(32), comment="用户组介绍")
    __table_args__ = ({'comment': '用户组'})


# 用户角色关联表
class UserRole(Base):
    __tablename__ = "sys_user_role"
    user = Column(VARCHAR(10), ForeignKey("user.id"), comment="用户ID")
    role = Column(VARCHAR(10), ForeignKey("role.id"), comment="角色ID")

    __table_args__ = ({'comment': '用户角色关联表'})


# 用户组角色表
class UserGroupRole(Base):
    __tablename__ = "sys_user_group_role"
    user_group = Column(VARCHAR(10), ForeignKey("user_group.id"), comment="用户组ID")
    role = Column(VARCHAR(10), ForeignKey("role.id"), comment="角色ID")
    __table_args__ = ({'comment': ' 用户组—角色表'})


# 用户组用户表
class UserGroupUser(Base):
    __tablename__ = "sys_user_group_user"
    user_group = Column(VARCHAR(10), ForeignKey("user_group.id"),
                        comment="用户组ID")
    role = Column(VARCHAR(10), ForeignKey("role.id"), comment="角色ID")
    __table_args__ = ({'comment': ' 用户组—用户表'})
