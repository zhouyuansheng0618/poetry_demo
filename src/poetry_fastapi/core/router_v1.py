'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/21 15:57
@Software: PyCharm
@File    : router_v1.py
'''

from fastapi import APIRouter
from poetry_fastapi.api.v1.category import router as category_router
from poetry_fastapi.api.v1.user import router as user_router
from poetry_fastapi.api.v1.role import router as role_router
from poetry_fastapi.api.v1.permission import router as permission_router

api_v1_router = APIRouter()
api_v1_router.include_router(category_router, prefix='/category', tags=['分类'])
api_v1_router.include_router(user_router, prefix='/user', tags=['用户'])
api_v1_router.include_router(role_router, prefix="/role", tags=['角色'])
api_v1_router.include_router(permission_router, prefix="/permission", tags=['权限'])
# api_v1_router.include_router(items_router, tags=["测试API"], dependencies=[Depends(check_jwt_token)])
# check_authority 权限验证内部包含了 token 验证 如果不校验权限可直接 dependencies=[Depends(check_jwt_token)]

# api_v1_router.include_router(items_router, tags=["测试接口"], dependencies=[Depends(check_authority)])
# api_v1_router.include_router(scheduler_router, tags=["任务调度"],  dependencies=[Depends(check_authority)])
# api_v1_router.include_router(sys_api_router, tags=["服务API管理"],  dependencies=[Depends(check_authority)])
# api_v1_router.include_router(sys_casbin_router, tags=["权限API管理"],  dependencies=[Depends(check_authority)])
