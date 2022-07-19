# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：users.py 
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/19 17:27
"""

import enum

from sqlalchemy import *

from poetry_fastapi.db.base import Base


# 用户表
class UserMode(Base):
    __tablename__ = "sys_user"
    salt = Column(VARCHAR(6), comment="用户密码加盐")
    password = Column(VARCHAR(128), nullable=False, comment="密码")
    last_login = Column(DateTime, blank=True, null=True, comment="密码")
    is_superuser = Column(Integer, default=0, comment="超级用户:0=N,1=Y", server_default='0')
    is_staff = Column(Integer, default=0, comment="超级用户:0=N,1=Y", server_default='0')



class PostMode(Base):
    __tablename__ = "sys_post"
    name = Column(VARCHAR(64), comment="岗位名称", null=False)
    code = Column(VARCHAR(6), comment="岗位编码", null=False)
    sort = Column(Integer, default=1, comment="岗位顺序", null=False)

