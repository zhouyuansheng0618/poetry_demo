"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：session.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/1 22:22
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from poetry_fastapi.config.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

