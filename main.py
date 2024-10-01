# -*- coding = utf-8 -*-
# @Time : 2024/10/1 0001 22:50
# @Author : SleepCat
# @File : main.py
# @Software : PyCharm


import json
from flask import Flask, request

from api import iphoneData

app = Flask(__name__)


@app.route("/")
def index():
    return "hello world"


@app.route("/api")
def api():
    return "None"


@app.route("/api/iphone_data")
def iphone_data():
    if request.args is None:
        return "未提供参数"

    args: dict = request.args.to_dict()

    if args.get("imei") is None:
        return "未提供imei"
    else:
        imei = args.get("imei")

    if args.get("type") is None:
        return "未提供type"
    else:
        _type = args.get("type")

    if _type == "json":
        response = json.dumps(iphoneData.getData(imei)).encode("utf-8").decode("utf-8")
    elif _type == "txt":
        data = iphoneData.getData(imei).get('data')
        response = "<pre>" \
                   f"IMEI/SN: {data.get('IMEI/SN')}\n" \
                   f"设备型号: {data.get('设备型号')}\n" \
                   f"容量: {data.get('容量')}\n" \
                   f"颜色: {data.get('颜色')}" \
                   "</pre>"

    return response.encode("utf-8")


if __name__ == '__main__':
    app.run(port=10000)


