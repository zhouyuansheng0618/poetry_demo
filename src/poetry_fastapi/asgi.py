# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：asgi.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/13 21:39
"""
# from .main import get_app
#
# app = get_app()
from skywalking import agent, config as sky_config

# config.disable_plugins = ['sw_http_server', 'sw_urllib_request','sw_django','sw_tornado','sw_urllib3','sw_sanic','sw_aiohttp','sw_pyramid']#也可以排除一些不想纳入跟踪的组件
sky_config.init(collector_address='10.113.163.105:8013', service_name='songling')  # 采集服务的地址，给自己的服务起个名称
# flask接收到的http参数也保存
sky_config.fastapi_collect_http_params = True
agent.start()

from poetry_fastapi.core.server import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    # 输出所有的路由
    # for route in app.routes:
    #     if hasattr(route, "methods"):
    #         print(
    #             {'path': route.__dict__['path'], 'name': route.__dict__['name'], 'methods': route.__dict__['methods']})
    #
    # uvicorn.run(app='main:app', host="0.0.0.0", port=8010, reload=True, debug=True)
    from skywalking import agent, config as sky_config
    sky_config.init(collector_address='10.122.146.139:11800', service_name='ifthen1')
    agent.start()

    # uvicorn.run(app=app, host="0.0.0.0", port=9103, ssl_keyfile="./ssl/st2.key", ssl_certfile="./ssl/st2.crt")
    uvicorn.run(app=app, host="0.0.0.0", port=9103)
