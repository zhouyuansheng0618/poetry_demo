# -*- coding: utf-8 -*- 
# @Time : 2022/7/8 11:45 
# @Author : zhouys618@163.com 
# @File : user.py 
# @desc:
from typing import Any

from fastapi import APIRouter, Depends, Body
from fastapi.encoders import jsonable_encoder

from poetry_fastapi.common import response_code, resp
from poetry_fastapi.common.deps import *
from poetry_fastapi.common.get_db import get_db
from poetry_fastapi.common.security import create_access_token
from poetry_fastapi.crud.user import crud_user
from poetry_fastapi.models.user import *
from poetry_fastapi.schemas.user import *
from sqlalchemy.orm import Session

from poetry_fastapi.utils.encrypt import encryption_password_or_decode

router = APIRouter()


@router.post("/user", summary="创建用户", response_model=CreateUser)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    is_user = crud_user.get_name(db, name=user.name)
    if is_user:
        return response_code.resp_4005(message="用户已存在")
    user_data = crud_user.create(db, obj_in=user)
    return response_code.resp_200(data=user_data, message="创建用户成功")


@router.get("/user/all", summary="查询未删除的所有用户")
def user_not_delete_list(db: Session = Depends(get_db),
                         skip: str = 0,
                         limit: int = 20):
    filters = [User.is_delete == 0]
    user_data = crud_user.get_multi(db, skip=skip, limit=limit, filter=filters)
    return response_code.resp_200(data=user_data)


@router.get("/delete/all", summary="查询删除的所有用户")
def user_delete_list(db: Session = Depends(get_db),
                     skip: str = 0,
                     limit: int = 20):
    filters = [User.is_delete == 1]

    user_data = crud_user.get_multi(db, skip=skip, limit=limit, filter=filters)
    return response_code.resp_200(data=user_data)



@router.get("/info", summary="获取用户信息", response_model=RespUserInfo)
def get_user_info(*, user: User = Depends(get_current_user)) -> Any:
    user_data = {
        "roles": ['admin'],
        "introduction": '',
        "name": user.name,
        "mobile": user.mobile,
        "create_time": user.create_time,
        "head_img_url": user.head_img_url,
        "avatar": 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    }
    return response_code.resp_200(data=user_data)


@router.get("/user/get", summary="查看用户详情")
def get_user_id_or_mobile_or_name(db: Session = Depends(get_db),
                                  id: str = None,
                                  mobile: str = None,
                                  name: str = None) -> Any:
    filters = [User.state == 0, User.is_delete == 0]
    if id:
        filters.append(User.id == id)
    if mobile:
        filters.append(User.mobile == mobile)
    if name:
        filters.append(User.name == name)
    user_info = crud_user.get_query(db, filters)
    return response_code.resp_200(data=user_info)


@router.delete("/user", summary="删除用户")
def delete_user(user: DeleteUser, db: Session = Depends(get_db)) -> Any:
    _user = crud_user.remove(db, id=user.id)
    if _user:
        return response_code.resp_200(message="删除成功")


@router.put("/user", summary="修改用户信息")
def put_user(db: Session = Depends(get_db),
             password: str = Body(None),
             mobile: str = Body(None),
             head_img_url: str = Body(None),
             is_delete: int = Body(None),
             current_user: User = Depends(get_current_active_user)
             ) -> Any:
    if is_delete not in [0, 1, None]:
        return response_code.resp_4005(message="参数错误")

    current_user_data = jsonable_encoder(current_user)
    user_in = UpdateUser(**current_user_data)

    if password is not None:
        user_in.hashed_password, user_in.salt = encryption_password_or_decode(pwd=password)
    if mobile is not None:
        user_in.mobile = mobile
    if head_img_url is not None:
        user_in.head_img_url = head_img_url
    if is_delete is not None:
        user_in.is_delete = is_delete

    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)

    return response_code.resp_200(data=user)


@router.post("/login", summary="登录")
def login(curd_user: BaseUser, db: Session = Depends(get_db)) -> Any:
    user = crud_user.authenticate(db, phone=curd_user.username, password=curd_user.password)
    if not user:
        return response_code.resp_4005(message="用户名或密码错误或用户被禁用")
    sub = {
        "uid": user.id
    }
    token = create_access_token(subject=sub)
    return response_code.resp_200(data={"token": token})
