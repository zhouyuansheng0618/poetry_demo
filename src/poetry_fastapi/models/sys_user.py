# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：sys_user.py 
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/21 13:54
"""
# -*- coding: utf-8 -*-
from sqlalchemy.orm import relationship

"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：user.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/13 22:56
"""
import datetime
from poetry_fastapi.db.base_class import Base, gen_nanoid
from sqlalchemy import Column, Boolean, Integer, String, VARCHAR, Date, \
    ForeignKey
from nanoid import non_secure_generate


def get_nanoid() -> str:
    """
    生成nanoid 长度5
    """
    return non_secure_generate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", size=5)


def account_nanoid() -> str:
    """
    生成nanoid 长度5
    """
    return non_secure_generate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", size=8)


# 用户表
class User(Base):
    __tablename__ = "user"
    __table_args__ = ({'comment': '用户表'})
    state = Column(Integer, default=False, comment="用户状态:0=正常,1=禁用",
                   server_default="0")
    username = Column(String(32), unique=True, index=True, nullable=False, doc="编码")
    nickname = Column(String(32), doc="姓名")
    sex = Column(String(8), doc="性别")
    identity_card = Column(String(32), doc="身份证")
    phone = Column(String(32), doc="手机号")
    address = Column(String(32), doc="地址")
    work_start = Column(Date, doc="入职日期", default=datetime.datetime.today())
    hashed_password = Column(String(128), nullable=False, doc="密码")
    avatar = Column(String(128), doc="用户图像地址")
    introduction = Column(String(256), doc="自我介绍")
    status = Column(String(32), nullable=False, doc="状态")
    is_active = Column(Boolean(), default=True, doc="是否活跃")
    is_superuser = Column(Boolean(), default=False, doc="是否超级管理员")
    salt = Column(String(6), comment="用户密码加盐")

    user_role = relationship("UserRole", backref="user")
    user_department = relationship("UserDepartment", backref="user")
    user_dict = relationship("UserDict", backref="user")

class UserRole(Base):
    """用户-权限组-中间表"""
    __tablename__ = "user_role"
    __table_args__ = ({'comment': '用户-权限组-中间表'})
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    role_id = Column(Integer, ForeignKey("role.id"))

    role = relationship("Role")


class UserDepartment(Base):
    """用户-部门-中间表"""
    __tablename__ = "user_department"
    __table_args__ = ({'comment': '用户-部门-中间表'})
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    department_id = Column(Integer, ForeignKey("department.id"))

    department = relationship("Department")


class UserDict(Base):
    """用户-字典-中间表"""
    __tablename__ = "user_department"
    __table_args__ = ({'comment': '用户-字典-中间表'})
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    dict_id = Column(Integer, ForeignKey("dict_data.id", ondelete='CASCADE'))

    dict_data = relationship("DictData", backref="user_dict")


