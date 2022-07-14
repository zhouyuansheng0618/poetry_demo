'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/21 15:55
@Software: PyCharm
@File    : server.py
'''

import traceback


from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, ValidationError
from poetry_fastapi.config.config import settings
from poetry_fastapi.common.logger import logger
from poetry_fastapi.common import custom_exc, response_code
from poetry_fastapi.common.schedule import schedule
from poetry_fastapi.core.router_v1 import api_v1_router
from poetry_fastapi.db.redis import redis_client
from poetry_fastapi.db.session import db
from poetry_fastapi.common import resp
def create_app() -> FastAPI:
    """
    生成FatAPI对象
    :return:
    """
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        redoc_url=settings.REDOC_URL
    )

    # 其余的一些全局配置可以写在这里 多了可以考虑拆分到其他文件夹

    # 跨域设置
    register_cors(app)

    # 注册路由
    register_router(app)

    # 注册捕获全局异常
    register_exception(app)

    # 请求拦截
    register_hook(app)

    # 取消挂载在 request对象上面的操作，感觉特别麻烦，直接使用全局的
    register_init(app)

    if settings.DEBUG:
        # 注册静态文件
        register_static_file(app)

    return app


def register_static_file(app: FastAPI) -> None:
    """
    静态文件交互开发模式使用
    生产使用 nginx 静态资源服务
    这里是开发是方便本地
    :param app:
    :return:
    """
    import os
    from fastapi.staticfiles import StaticFiles
    if not os.path.exists("./static"):
        os.mkdir("./static")
    app.mount("/static", StaticFiles(directory="static"), name="static")


def register_router(app: FastAPI) -> None:
    """
    注册路由
    :param app:
    :return:
    """
    # 项目API
    app.include_router(
        api_v1_router,
    )


def register_cors(app: FastAPI) -> None:
    """
    支持跨域
    :param app:
    :return:
    """
    if settings.DEBUG:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def register_exception(app: FastAPI) -> None:
    """
    全局异常捕获
    注意 别手误多敲一个s
    exception_handler
    exception_handlers
    两者有区别
        如果只捕获一个异常 启动会报错
        @exception_handlers(UserNotFound)
    TypeError: 'dict' object is not callable
    :param app:
    :return:
    """

    # 自定义异常 捕获
    @app.exception_handler(custom_exc.TokenExpired)
    async def user_not_found_exception_handler(request: Request, exc: custom_exc.TokenExpired):
        """
        token过期
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"token未知用户\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

        return resp.fail(message=exc.err_desc)

    @app.exception_handler(custom_exc.TokenAuthError)
    async def user_token_exception_handler(request: Request, exc: custom_exc.TokenAuthError):
        """
        用户token异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"用户认证异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

        return resp.fail(resp.DataNotFound.set_msg(exc.err_desc))

    @app.exception_handler(custom_exc.AuthenticationError)
    async def user_not_found_exception_handler(request: Request, exc: custom_exc.AuthenticationError):
        """
        用户权限不足
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"用户权限不足 \nURL:{request.method}{request.url}")
        return resp.fail(resp.PermissionDenied)

    @app.exception_handler(ValidationError)
    async def inner_validation_exception_handler(request: Request, exc: ValidationError):
        """
        内部参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"内部参数验证错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return resp.fail(resp.BusinessError.set_msg(exc.errors()))

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        请求参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"请求参数格式错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        # return response_code.resp_4001(message='; '.join([f"{e['loc'][1]}: {e['msg']}" for e in exc.errors()]))
        return resp.fail(resp.InvalidParams.set_msg(exc.errors()))

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        全局所有异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"全局异常\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return resp.fail(resp.ServerError)


def register_hook(app: FastAPI) -> None:
    """
    请求响应拦截 hook
    https://fastapi.tiangolo.com/tutorial/middleware/
    :param app:
    :return:
    """

    @app.middleware("http")
    async def logger_request(request: Request, call_next) -> Response:
        # https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip
        # logger.info(f"访问记录:{request.method} url:{request.url}\nheaders:{request.headers}\nIP:{request.client.host}")
        response = await call_next(request)
        return response


def register_init(app: FastAPI) -> None:
    """
    初始化连接
    :param app:
    :return:
    """

    @app.on_event("startup")
    async def init_connect():
        # 连接redis
        # redis_client.init_redis_connect()

        # 初始化 apscheduler
        schedule.init_scheduler()

        db.connect()

    @app.on_event('shutdown')
    async def shutdown_connect():
        """
        关闭
        :return:
        """
        schedule.shutdown()

        if not db.is_closed():
            db.close()

