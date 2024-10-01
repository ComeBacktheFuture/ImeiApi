# -*- coding = utf-8 -*-
# @Time : 2024/10/1 0001 22:50
# @Author : SleepCat
# @File : main.py
# @Software : PyCharm


from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "hello world"


@app.route("/api")
def api():
    return ...


if __name__ == '__main__':
    app.run()


