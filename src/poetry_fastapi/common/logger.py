'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/17 22:42
@Software: PyCharm
@File    : logger.py
'''

import os

from loguru import logger

from poetry_fastapi.config.config import settings


def logs_path():
    # 获取当前文件夹
    current_path = os.path.dirname(__file__)

    # 获取当前文件夹的上一层文件
    base_path = os.path.abspath(os.path.join(current_path, ".."))

    # 拼接日志的路径
    log_path = base_path + os.sep + settings.LOGGER_FOLDER + os.sep
    # print(f'日志文件夹名: {log_path} \n')

    """如果文件夹不存在就创建"""
    os.makedirs(log_path, exist_ok=True)

    return log_path


""" 保留日志文件夹下最大个数(自己调试用) """
file_list = os.listdir(logs_path())
if len(file_list) > 4:
    os.remove(os.path.join(logs_path(), file_list[0]))

# 日志输出路径
log_path_name = os.path.join(logs_path(), settings.LOGGER_NAME)

# 详见: https://loguru.readthedocs.io/en/stable/overview.html#features
logger.add(log_path_name,
           encoding=settings.LOGGER_ENCODING,
           level=settings.LOGGER_LEVEL,
           rotation=settings.LOGGER_ROTATION,
           retention=settings.LOGGER_RETENTION,
           enqueue=True)

