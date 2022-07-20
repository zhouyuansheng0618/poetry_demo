# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：role.py 
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/18 11:11
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from poetry_fastapi.common.deps import get_db
from poetry_fastapi.crud.role import crud_role
from poetry_fastapi.common import response_code
from poetry_fastapi.schemas.role import *

router = APIRouter()


# 创建角色
@router.post("/create", summary="创建角色")
def create_role(role: CreateRole, db: Session = Depends(get_db)):
    is_role = crud_role.get_role_name(db, name=role.name)
    if is_role:
        return response_code.resp_4005(message="角色已存在")
    role = crud_role.role_create(db, obj_in=role)
    return response_code.resp_200(data=role)


# 修改角色
def update_role():
    pass


# 删除角色
def delete_role():
    pass


# 查询所有未删除角色
@router.get("/all", summary="查询所有")
def get_is_delete_all_role(db: Session = Depends(get_db)):
    role = crud_role.get_all(db)
    print(role)
    return response_code.resp_200(data={})


# 查询删除角色
def get_delete_all_role():
    pass
