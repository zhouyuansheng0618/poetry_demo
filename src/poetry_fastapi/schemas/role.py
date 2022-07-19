# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：role.py 
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/19 15:38
"""
from typing import Optional

from pydantic import BaseModel


class BaseRole(BaseModel):
    name: Optional[str] = None


class CreateRole(BaseRole):
    intro: Optional[str] = None

