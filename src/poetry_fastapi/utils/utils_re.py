# -*- coding: utf-8 -*- 
# @Time : 2022/7/15 15:57 
# @Author : zhouys618@163.com 
# @File : utils_re.py 
# @desc:
import re


def is_phone(arg):
    """
    判断是否是手机号
    :param arg:
    :param phone:
    :return: bool
    """
    pattern = re.compile(r'^(13[0-9]|14[0|5|6|7|9]|15[0|1|2|3|5|6|7|8|9]|'
                         r'16[2|5|6|7]|17[0|1|2|3|5|6|7|8]|18[0-9]|'
                         r'19[1|3|5|6|7|8|9])\d{8}$')
    return True if pattern.search(arg) else False


def is_mail(arg):
    """
    判断是否是邮箱
    :param arg:
    :return:
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return True if re.fullmatch(regex, arg) else False
