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
class User(Base):
    __tablename__ = "user"
    state = Column(Integer, default=False, comment="用户状态:0=正常,1=禁用",
                   server_default="0")
    name = Column(VARCHAR(64), nullable=False, comment="用户名")
    head_img_url = Column(VARCHAR(255), comment="用户图像地址")
    mobile = Column(VARCHAR(11), unique=True, index=True,
                    comment="手机号")
    salt = Column(VARCHAR(64), comment="用户密码加盐")
    hashed_password = Column(VARCHAR(128), nullable=False, comment="密码")
    creator = Column(VARCHAR(36), nullable=True, comment="创建人")
    editor = Column(VARCHAR(36), nullable=True, comment="修改人")
    __table_args__ = ({'comment': '用户表'})