# -*- coding: utf-8 -*- 
# @Time : 2022/7/14 14:53 
# @Author : zhouys618@163.com 
# @File : test_password.py 
# @desc:

from passlib.context import CryptContext
def encryption_password_or_decode(*, pwd: str,salt:str, hashed_password: str = None):
    """
    密码加密或解密
    :param pwd:
    :param hashed_password:
    :return:
    """
    encryption_pwd = CryptContext(
        schemes=["sha256_crypt", "md5_crypt", "des_crypt"],
        deprecated="auto"
    )

    def encryption_password():
        password = encryption_pwd.hash(pwd+salt)
        return password

    def decode_password():
        password = encryption_pwd.verify(pwd+salt, hashed_password)
        return password

    return decode_password() if hashed_password else encryption_password()
encryption_pwd = CryptContext(
    schemes=["sha256_crypt", "md5_crypt", "des_crypt"]
)
def decode_password(pwd,salt,hashed_password):
    password = encryption_pwd.verify(pwd+salt, hashed_password)
    return password

if __name__ == '__main__':

    decode_password(pwd='admin',salt='JL2lAy',hashed_password='$5$rounds=535000$YauKkhm0XXGJ/pyA$sSXDA48tI/il4tkmeFr0F1fodgkHudwwNNFOKuJuQo8')


