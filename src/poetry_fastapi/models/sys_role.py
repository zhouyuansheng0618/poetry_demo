# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：sys_role.py 
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/21 15:52
"""
import datetime

from sqlalchemy.orm import relationship

from poetry_fastapi.db.base_class import Base, gen_nanoid
from sqlalchemy import Column, Boolean, Integer, String, VARCHAR, Date, \
    ForeignKey
from nanoid import non_secure_generate


def get_nanoid() -> str:
    """
    生成nanoid 长度5
    """
    return non_secure_generate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", size=5)


# 角色表
class Role(Base):
    """权限组"""
    __tablename__ = "sys_role"
    __table_args__ = ({'comment': '角色表'})
    code = Column(String(5), default=get_nanoid, comment="角色唯一CODE代码")
    name = Column(String(32), doc="权限组名称")
    description = Column(String(128), doc="备注")
    order = Column(Integer, doc="顺序")

    role_menu = relationship("Role_Menu", backref="role")


class RoleMenu(Base):
    """权限组-菜单-中间表"""
    __tablename__ = "sys_role_menu"
    __table_args__ = ({'comment': ' 权限组-菜单-中间表'})
    role_id = Column(Integer, ForeignKey("role.id", ondelete='CASCADE'))
    menu_id = Column(Integer, ForeignKey("menu.id", ondelete='CASCADE'))
