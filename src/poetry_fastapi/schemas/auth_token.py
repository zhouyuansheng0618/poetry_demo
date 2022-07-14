# -*- coding: utf-8 -*- 
# @Time : 2022/7/14 18:14 
# @Author : zhouys618@163.com 
# @File : token.py 
# @desc:
from typing import Optional

from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: Optional[dict] = None