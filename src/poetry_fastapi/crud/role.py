# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：role.py 
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/20 13:55
"""
from sqlalchemy.orm import Session

from poetry_fastapi.crud.base import CrudBase
from poetry_fastapi.models.user import Role
from poetry_fastapi.schemas.role import *


class CrudRole(CrudBase[Role, CreateRole, UpdateRole]):
    @staticmethod
    def get_role_all(db: Session) -> Optional[Role]:
        return db.query(Role).all()

    @staticmethod
    def get_role_name(db: Session, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).all()

    @staticmethod
    def role_create(db: Session, *, obj_in: CreateRole) -> Optional[Role]:
        db_obj = Role(
            name=obj_in.name,
            intro=obj_in.intro
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_role = CrudRole(Role)
