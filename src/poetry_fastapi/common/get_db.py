# -*- coding: utf-8 -*- 
# @Time : 2022/7/14 14:05 
# @Author : zhouys618@163.com 
# @File : get_db.py 
# @desc:
from poetry_fastapi.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()