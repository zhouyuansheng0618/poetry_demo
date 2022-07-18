'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/21 15:59
@Software: PyCharm
@File    : deps.py
'''
from poetry_fastapi.crud.user import crud_user
from poetry_fastapi.schemas.auth_token import TokenPayload

"""

一些通用的依赖功能

"""
from typing import Generator, Any, Union, Optional
#
from jose import jwt
from pydantic import ValidationError

from poetry_fastapi.common import custom_exc
from poetry_fastapi.models.user import User
from poetry_fastapi.config.config import settings
from sqlalchemy.orm import Session
from fastapi import Header, Depends, HTTPException

from poetry_fastapi.common.get_db import get_db


def check_jwt_token(
        token: Optional[str] = Header(..., description="登录token")
) -> Union[str, Any]:
    """
    解析验证token  默认验证headers里面为token字段的数据
    可以给 headers 里面token替换别名, 以下示例为 X-Token
    token: Optional[str] = Header(None, alias="X-Token")
    :param token:
    :return:
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise custom_exc.TokenExpired()
    except (jwt.JWTError, ValidationError, AttributeError):
        raise custom_exc.TokenAuthError()


def get_current_user(
        db: Session = Depends(get_db),
        token: Optional[str] = Header(None, alias="X-Token")
) -> User:
    """
    根据header中token 获取当前用户
    :param db:
    :param token:
    :return:
    """
    if not token:
        raise custom_exc.UserTokenError(err_desc='headers not found token')
    token_data = check_jwt_token(token)
    uid = eval(token_data.get('sub')).get("uid")
    user = crud_user.get(db, id=uid)
    if not user:
        raise custom_exc.TokenAuthError(err_desc="User not found")
    return user


def get_current_active_user(
        current_user: User = Depends(get_current_user),
) -> User:
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NTg0ODI0MTMsInN1YiI6InsndWlkJzogJ2ZhV3NYZUZGclR6Zid9IiwiYXV0aG9yaXR5X2lkIjpudWxsfQ.qyAMRx9FUFwlPMKRctyGza7nZShqhtd-BIC1iNU38mw"  # print(get_user(token=token))
    print(check_jwt_token(token))
