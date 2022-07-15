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
    username: str = Field(min_length=2, max_length=32)
    password: str = Field(min_length=6, max_length=18)



class CreateUser(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    phone: str = Field(min_length=11, max_length=11)
    password: str = Field(min_length=6, max_length=18)


class UpdateUser(BaseUser):
    pass


class DeleteUser(BaseUser):
    pass


class QueryUser(BaseUser):
    pass


class UserInfo(BaseModel):
    name: str
    mobile: str
    state: int
    head_img_url: str

    # 响应体中的字段 不设置为TRUE 则返回所有字段

    class Config:
        orm_mode = True


class RespUserInfo(BaseResp):
    # 响应用户信息
    data: UserInfo
