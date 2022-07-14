# -*- coding: utf-8 -*-
# @Author : zhouys
# @Contact:zhouys618@163.com
# @Software : blog_server
# @File : blog_tag
# @Time : 2021/12/21 22:13
from typing import Any, Optional
from fastapi import APIRouter, Depends

from poetry_fastapi.common import deps, response_code




router = APIRouter()


@router.get("/create_category", summary="创建文章分类")
def category_create() -> Any:
    add_category=[]
    return response_code.resp_200(data=add_category, message="文章分类创建成功")









