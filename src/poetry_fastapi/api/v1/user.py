# -*- coding: utf-8 -*- 
# @Time : 2022/7/8 11:45 
# @Author : zhouys618@163.com 
# @File : user.py 
# @desc:
from typing import Any

from fastapi import APIRouter, Depends
from poetry_fastapi.common import response_code, resp
from poetry_fastapi.common.deps import get_current_user
from poetry_fastapi.common.get_db import get_db
from poetry_fastapi.common.security import create_access_token
from poetry_fastapi.crud.user import crud_user
from poetry_fastapi.models.user import *
from poetry_fastapi.schemas.user import *
from sqlalchemy.orm import Session

from poetry_fastapi.utils.utils_re import *

router = APIRouter()


@router.get("/user/all", summary="查询所有用户")
def user_list(db: Session = Depends(get_db),
              skip: str = 0,
              limit: int = 20):
    user_data = crud_user.get_multi(db, skip=skip, limit=limit)
    return response_code.resp_200(data=user_data)


@router.post("/user", summary="创建用户", response_model=CreateUser)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    is_user = crud_user.get_name(db, name=user.name)
    if is_user:
        return response_code.resp_4005(message="用户已存在")
    user_data = crud_user.create(db, obj_in=user)
    return response_code.resp_200(data=user_data, message="创建用户成功")


@router.get("/user/info", summary="获取用户信息", response_model=RespUserInfo)
def get_user_info(*, user: User = Depends(get_current_user)) -> Any:
    user_data = {
        "name": user.name,
        "mobile": user.mobile,
        "create_time": user.create_time,
        "head_img_url": user.head_img_url,
    }
    return response_code.resp_200(data=user_data)


@router.get("/user/get", summary="用户信息")
def get_user_id_or_mobile_or_name(db: Session = Depends(get_db),
                                  id: str = None,
                                  mobile: str = None,
                                  name: str = None) -> Any:
    filters = []
    filters.append(User.state != 1)
    filters.append(User.is_delete != 1)
    if id:
        filters.append(User.id == id)
    if mobile:
        filters.append(User.mobile == mobile)
    if name:
        filters.append(User.name == name)
    user_info = crud_user.get_query(db, filters)
    return response_code.resp_200(data=user_info)


@router.post("/login", summary="登录")
def login(user: BaseUser, db: Session = Depends(get_db)) -> Any:
    user = crud_user.authenticate(db, name=user.username, password=user.password)
    if not user:
        return response_code.resp_4005(message="用户名或密码错误或用户被禁用")
    sub = {
        "uid": user.id
    }
    token = create_access_token(subject=sub)
    return response_code.resp_200(data={"token": token})

# def logout():
#     pass
