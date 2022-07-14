# -*- coding: utf-8 -*- 
# @Time : 2022/7/8 13:43 
# @Author : zhouys618@163.com 
# @File : user.py 
# @desc:
from datetime import datetime
from pydantic import Field, BaseModel, validator
from typing import Optional, List
from poetry_fastapi.schemas.base import BaseResp, ResAntTable


class BaseUser(BaseModel):
    username: str = Field(min_length=3, max_length=10)
    password: str = Field(min_length=6, max_length=12)


class CreateUser(BaseModel):
    name: str
    mobile: str
    password: str


class UpdateUser(BaseUser):
    pass


class DeleteUser(BaseUser):
    pass


class QueryUser(BaseUser):
    pass


class UserInfo(BaseModel):
    name: str
