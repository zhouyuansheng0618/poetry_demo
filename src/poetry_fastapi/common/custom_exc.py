'''
-*- coding: utf-8 -*-
@Author  : zhouys
@Time    : 2021/11/17 23:01
@Software: PyCharm
@File    : custom_exc.py
'''
"""
自定义异常
"""
class UserTokenError(Exception):
    def __init__(self, err_desc: str = "用户认证异常"):
        self.err_desc = err_desc


class UserNotFound(Exception):
    def __init__(self, err_desc: str = "没有此用户"):
        self.err_desc = err_desc


class PostParamsError(Exception):
    def __init__(self, err_desc: str = "POST请求参数错误"):
        self.err_desc = err_desc

class TokenAuthError(Exception):
    def __init__(self, err_desc: str = "User Authentication Failed"):
        self.err_desc = err_desc


class TokenExpired(Exception):
    def __init__(self, err_desc: str = "Token has expired"):
        self.err_desc = err_desc


class AuthenticationError(Exception):
    def __init__(self, err_desc: str = "Permission denied"):
        self.err_desc = err_desc
