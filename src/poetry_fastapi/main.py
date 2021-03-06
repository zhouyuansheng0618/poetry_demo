# -*- coding: utf-8 -*-
"""
@Auth ： zhouys
@Email:zhouys618@163.com
@File ：main.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Time ： 2022/7/13 20:43
"""
# from fastapi import FastAPI
#
# def get_app():
#     app = FastAPI(title="GINO FastAPI Demo")
#
#     return app

from poetry_fastapi.core.server import create_app

app = create_app()
if __name__ == "__main__":
    import uvicorn

    # 输出所有的路由
    for route in app.routes:
        if hasattr(route, "methods"):
            print(
                {'path': route.__dict__['path'], 'name': route.__dict__['name'], 'methods': route.__dict__['methods']})

    uvicorn.run(app='main:app', host="127.0.0.1", port=8010, reload=True, debug=True)
