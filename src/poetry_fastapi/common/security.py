'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/17 22:55
@Software: PyCharm
@File    : security.py
'''


"""
token password 验证
pip install python-jose
pip install passlib
pip install bcrypt

"""
from typing import Any, Union
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from poetry_fastapi.config.config import settings

pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])


def create_access_token(
        subject: Union[str, Any],
        authority_id: str = None,
        expires_delta: timedelta = None
) -> str:
    """
    生成token
    :param subject:需要存储到token的数据(注意token里面的数据，属于公开的)
    :param authority_id: 权限id(用于权限管理)
    :param expires_delta:
    :return:
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "authority_id": authority_id}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

from nanoid import generate


def gen_nanoid() -> str:
    """
    生成nanoid 长度6
    """
    return generate(size=6)




if __name__ == '__main__':
    print(create_access_token(subject={"id":"NEbkzL21mHiq"}))

"""
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NTg3MzkzNDgsInN1YiI6InsnaWQnOiAnTkVia3pMMjFtSGlxJ30iLCJhdXRob3JpdHlfaWQiOm51bGx9.4rDZ8JiPtoC4ufZny234VasmpFZZNUJMWX8TtgTbJik
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NTg3MTcwMjgsInN1YiI6InsnaWQnOiAnaFZ1WFpXRTFxTHJpJ30iLCJhdXRob3JpdHlfaWQiOm51bGx9.XZe57KNyOJZGHgbx_9HJYZFwfCcQigTIi88vcur2xNw
"""