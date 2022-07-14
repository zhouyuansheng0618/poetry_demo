# -*- coding: utf-8 -*- 
# @Time : 2022/7/14 14:13 
# @Author : zhouys618@163.com 
# @File : user.py 
# @desc:
from typing import Optional

from sqlalchemy.orm import Session
from poetry_fastapi.crud.base import CrudBase
from poetry_fastapi.models.user import *
from poetry_fastapi.schemas.user import CreateUser, UpdateUser
from poetry_fastapi.utils.encrypt import encryption_password_or_decode


class CrudUser(CrudBase[User, CreateUser, UpdateUser]):

    @staticmethod
    def get_all(db: Session) -> Optional[User]:
        return db.query(User).all()

    def get_id(self, db: Session, id: str = None) -> Optional[User]:
        return db.query(User).filter(id=id).first()

    def create(self, db: Session, *, obj_in: CreateUser) -> Optional[User]:
        hash_password, salt = encryption_password_or_decode(pwd=obj_in.password)
        db_obj = User(
            name=obj_in.name,
            head_img_url='',
            mobile=obj_in.mobile,
            salt=salt,
            hashed_password=hash_password
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_user = CrudUser(User)
