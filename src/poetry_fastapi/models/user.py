# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：user.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/13 22:56
"""
from poetry_fastapi.db.base_class import Base, gen_nanoid
from sqlalchemy import Column, Boolean, Integer, String, VARCHAR, BIGINT, \
    ForeignKey


# 用户表
class User(Base):
    __tablename__ = "user"
    state = Column(Integer, default=False, comment="用户状态:0=正常,1=禁用",
                   server_default="0")
    name = Column(VARCHAR(64), nullable=False, comment="用户名")
    head_img_url = Column(VARCHAR(255), comment="用户图像地址")
    mobile = Column(VARCHAR(11), unique=True, index=True,
                    comment="手机号")
    salt = Column(VARCHAR(6), comment="用户密码加盐")
    hashed_password = Column(VARCHAR(128), nullable=False, comment="密码")
    __table_args__ = ({'comment': '用户表'})


# 权限表
class Permission(Base):
    __tablename__ = "permission"
    parent_id = Column(VARCHAR(12), default=gen_nanoid, unique=True,
                       comment="所属父级权限ID")
    code = Column(VARCHAR(32), comment="权限唯一CODE代码")
    name = Column(VARCHAR(32), comment="权限名称")
    intro = Column(VARCHAR(32), comment="权限介绍")
    category = Column(VARCHAR(32), comment="权限类别")
    uri = Column(VARCHAR(255), comment="URL规则")
    __table_args__ = ({'comment': '权限表'})


# 角色表
class Role(Base):
    __tablename__ = "role"
    parent_id = Column(VARCHAR(12), default=gen_nanoid, comment="所属父级角色ID")
    code = Column(VARCHAR(32), comment="角色唯一CODE代码")
    name = Column(VARCHAR(32), comment="角色名称")
    intro = Column(VARCHAR(255), comment="角色介绍")
    __table_args__ = ({'comment': '角色表'})


# 用户组
class UserGroup(Base):
    __tablename__ = "user_group"
    parent_id = Column(VARCHAR(32), comment="所属父级用户组ID")
    name = Column(VARCHAR(32), comment="用户组名称")
    code = Column(VARCHAR(32), comment="用户组CODE唯一代码")
    intro = Column(VARCHAR(32), comment="用户组介绍")
    __table_args__ = ({'comment': '用户组'})


# 用户账号表
class Account(Base):
    __tablename__ = "account"
    user_id = Column(VARCHAR(10), ForeignKey("user.id"))  # 与用户表进行关联
    open_code = Column(VARCHAR(255), unique=True, nullable=True,
                       comment="登录账号，如手机号 微信号等")
    account = Column(VARCHAR(10), comment="账号", unique=True)
    category = Column(Integer, comment="账号类别", nullable=True)
    __table_args__ = ({'comment': '账号表'})


# 用户角色关联表
class UserRole(Base):
    __tablename__ = "user_role"
    user = Column(VARCHAR(10), ForeignKey("user.id"), comment="用户ID")
    role = Column(VARCHAR(10), ForeignKey("role.id"), comment="角色ID")

    __table_args__ = ({'comment': '用户角色关联表'})


# 用户组角色表
class UserGroupRole(Base):
    __tablename__ = "user_group_role"
    user_group = Column(VARCHAR(10), ForeignKey("user_group.id"), comment="用户组ID")
    role = Column(VARCHAR(10), ForeignKey("role.id"), comment="角色ID")
    __table_args__ = ({'comment': ' 用户组—角色表'})


# 用户组用户表
class UserGroupUser(Base):
    __tablename__ = "user_group_user"
    user_group = Column(VARCHAR(10), ForeignKey("user_group.id"),
                        comment="用户组ID")
    role = Column(VARCHAR(10), ForeignKey("role.id"), comment="角色ID")
    __table_args__ = ({'comment': ' 用户组—用户表'})


# 角色权限关联表
class RolePermission(Base):
    __tablename__ = "role_permission"
    role = Column(VARCHAR(10), ForeignKey("role.id"), comment="角色权限管理ID")
    permission = Column(VARCHAR(10), ForeignKey("permission.id"), comment="角色权限管理")
    __table_args__ = ({'comment': '角色权限关联表'})
