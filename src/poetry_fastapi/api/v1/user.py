# -*- coding: utf-8 -*- 
# @Time : 2022/7/8 11:45 
# @Author : zhouys618@163.com 
# @File : user.py 
# @desc:
from typing import Any

from fastapi import APIRouter, Query, Depends

from poetry_fastapi.common import response_code
from poetry_fastapi.common.deps import get_current_user
from poetry_fastapi.common.get_db import get_db
from poetry_fastapi.crud.user import crud_user
from poetry_fastapi.db.session import SessionLocal
from poetry_fastapi.models.user import *
from poetry_fastapi.schemas.user import *
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/user", summary="查询用户", response_model=UserInfo)
def user_list(db: Session = Depends(get_db)):
    user_data = crud_user.get_all(db)
    return response_code.resp_200(data=user_data, message="文章分类创建成功")


@router.post("/user", summary="创建用户", response_model=CreateUser)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user_data = crud_user.create(db, obj_in=user)
    return response_code.resp_200(data=user_data, message="创建用户成功")


@router.get("/user/info", summary="获取用户信息", response_model=RespUserInfo)
def get_user_info(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Any:
    user_data = {
        "name": current_user.name,
        "mobile": current_user.mobile,
        "create_time": current_user.create_time,
        "head_img_url": current_user.head_img_url,
    }
    return response_code.resp_200(data=user_data)
