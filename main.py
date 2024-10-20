# -*- coding = utf-8 -*-
# @Time : 2024/10/1 0001 22:50
# @Author : SleepCat
# @File : main.py
# @Software : PyCharm


import json
from pprint import pformat
from flask import Flask, request

from api import iphoneData
from api import GoogleRepairData
from api import SaltIphoneData
from api import UnlockApi

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

@app.route("/api/iphone_repair_data_test")
def iphone_repair_data_test():
    if request.args is None:
        return "未提供参数"

    args: dict = request.args.to_dict()

    if args.get("imei") is None:
        return "未提供imei"
    else:
        imei = args.get("imei")

    data = GoogleRepairData.getData(imei).get('data')
    text = "\n".join(k + ": " + str(v) for k, v in data.items())
    response = "<pre>\n" + text + "\n</pre>"

    return response.encode("utf-8")

@app.route("/api/iphone_active_data_test")
def iphone_active_data_test():
    if request.args is None:
        return "未提供参数"

    args: dict = request.args.to_dict()

    if args.get("imei") is None:
        return "未提供imei"
    else:
        imei = args.get("imei")

    response = SaltIphoneData.getData(imei)
    text = f"IMEI: {response['data']['IMEI']}\nFind My IPhone: {response['data']['Find My IPhone']}\n" \
           f"iCloudStatus: {response['data']['iCloudStatus']}" if response['code'] == 200 else \
           f"IMEI: {imei}\nFind My IPhone: None\n" \
           f"iCloudStatus: None"
    
    response = "<pre>\n" + text + "\n</pre>"

    return response.encode("utf-8")

@app.route("/api/iphone_unlock_code")
def iphone_unlock_code():
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

    response = UnlockApi.getData(imei)

    if _type == "json":
        response = json.dumps(response)
    elif _type == "txt":
        data = response.get('data')
        text = "\n".join(k + ": " + str(v) for k, v in data.items())
        response = "<pre>\n" + text + "\n</pre>"

    return response.encode("utf-8")



def init():
    GoogleRepairData.login(assount="unlockapi6@gmail.com", password="Aa123456@")


if __name__ == '__main__':
    init()
    app.run(host="0.0.0.0", port=10001)


