# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：config.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/13 22:45
"""
import os
from starlette.config import Config
from typing import Union, Optional

from pydantic import AnyHttpUrl, BaseSettings, IPvAnyAddress
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# config = Config(os.path.join(BASE_DIR, ".env"))
config = Config(".env")


class Settings(BaseSettings):
    # 开发模式配置
    DEBUG: bool = True
    # 项目文档
    TITLE: str = "FastAPI+MySQL项目生成"
    DESCRIPTION: str = "更多FastAPI知识，请关注我的个人网站 https://www.charmcode.cn/"
    # 文档地址 默认为docs 生产环境关闭 None
    DOCS_URL: str = "/docs"
    # 文档关联请求数据接口
    OPENAPI_URL: str = "/openapi.json"
    # redoc 文档
    REDOC_URL: Optional[str] = "/redoc"

    # token过期时间 分钟
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # 生成token的加密算法
    ALGORITHM: str = "HS256"

    # 生产环境保管好 SECRET_KEY
    SECRET_KEY: str = 'xxxxxxxx'

    # 项目根路径
    BASE_PATH: str = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))

    # 配置你的Mysql环境
    MYSQL_USERNAME: str = config("MYSQL_USERNAME", default="fastapi")
    MYSQL_PASSWORD: str = config("MYSQL_PASSWORD",default="")
    MYSQL_HOST: str = config("HOST",default='')
    MYSQL_PORT: int = config("PORT",default=3306)
    MYSQL_DATABASE: str = config("DATABASE",default="fastapi")
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@" \
                              f"{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4"
    # redis配置
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    REDIS_PORT: int = 6379
    REDIS_URL: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encoding=utf-8"
    REDIS_TIMEOUT: int = 5  # redis连接超时时间

    CASBIN_MODEL_PATH: str = "./resource/rbac_model.conf"
    # 日志文件夹名
    LOGGER_FOLDER = "logs"
    # 日志文件名 (时间格式)
    LOGGER_NAME = '{time:YYYY-MM-DD_HH-mm-ss}.log'
    LOGGER_ENCODING = 'utf-8'
    LOGGER_LEVEL = 'DEBUG'  # ['DEBUG' | 'INFO']
    # 按 时间段 切分日志
    LOGGER_ROTATION = "100 MB"  # ["500 MB" | "12:00" | "1 week"]
    # 日志保留的时间, 超出将删除最早的日志
    LOGGER_RETENTION = "1 days"  # ["1 days"]

settings = Settings()
