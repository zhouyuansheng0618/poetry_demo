# -*- coding: utf-8 -*- 
# @Time : 2022/7/14 14:09 
# @Author : zhouys618@163.com 
# @File : base.py 
# @desc:
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session


from poetry_fastapi.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_id(self, db: Session, id: str) -> Optional[ModelType]:
        """
        根据id查询
        :param db:
        :param id:
        :return:
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session) -> Optional[ModelType]:
        """
        查询所有
        :param db:
        :return:
        """
        return db.query(self.model).all()

    def get_query(self, db: Session, filters: Any) -> Optional[ModelType]:
        """
        条件查询所有
        :param db:
        :param filters:
        :return:
        """
        return db.query(self.model).filter(*filters).all()

    def get_query_count(self, db: Session, filters: Any) -> Optional[int]:
        """
        统计条数
        :param db:
        :param filters:
        :return:
        """
        return db.query(self.model).filter(*filters).count()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100, filters: Any
    ) -> List[ModelType]:
        """
        分页查询
        :param db:
        :param skip:
        :param limit:
        :param filters:
        :return:
        """
        return db.query(self.model).filter(*filters).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: str) -> ModelType:
        """
        假删除 修改状态
        :param db:
        :param id:
        :return:
        """
        obj = db.query(self.model).filter(self.model.id == id).update({"is_delete": 1})
        db.commit()
        return obj
