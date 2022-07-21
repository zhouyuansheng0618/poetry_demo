# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：test_fastdfs.py 
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/20 17:29
"""

from fdfs_client.client import *


class FastDfs(object):

    def __init__(self):
        self.client = Fdfs_client(get_tracker_conf('client.conf'))

    def upload(self, path):
        resp = self.client.upload_by_filename(path)
        for item in resp:
            if isinstance(resp[item], bytes):
                resp[item] = str(resp[item], encoding='utf8')
        return resp



if __name__ == '__main__':
    fast = FastDfs()

    # print(fast.upload(path='1.jpg'))



