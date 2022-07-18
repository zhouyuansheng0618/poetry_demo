# -*- coding: utf-8 -*- 
# @Time : 2022/7/14 14:34 
# @Author : zhouys618@163.com 
# @File : encrypt.py 
# @desc: 加密 解密

from nanoid import generate


def gen_nanoid() -> str:
    """
    生成nanoid 长度6
    """
    return generate(size=6)


from passlib.context import CryptContext


def encryption_password_or_decode(*, pwd: str, salt: str = None, hashed_password: str = None):
    """
    密码加密或解密
    :param pwd:
    :param hashed_password:
    :return:
    """
    encryption_pwd = CryptContext(
        schemes=["sha256_crypt", "md5_crypt", "des_crypt"]
    )

    def encryption_password():
        salt = gen_nanoid()
        password = encryption_pwd.hash(pwd + salt)

        return password, salt

    def decode_password():
        password = encryption_pwd.verify(pwd + salt, hashed_password)
        return password

    return decode_password() if hashed_password else encryption_password()
