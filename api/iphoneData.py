# -*- coding = utf-8 -*-
# @Time : 2024/10/1 0001 23:10
# @Author : SleepCat
# @File : iphoneData.py
# @Software : PyCharm


from requests import post

url = "https://www.iplace.com.br/ccstorex/custom/v1/hervalApiCalls/getData"

headers = {
    "authority": 'www.iplace.com.br',
    "method": 'POST',
    "path": '/ccstorex/custom/v1/hervalApiCalls/getData',
    "scheme": 'https',
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": 'no-cache',
    "content-length": "95",
    "content-type": "application/json; charset=UTF-8",
    "origin": 'https://www.iplace.com.br',
    'pragma': 'no-cache',
    "priority": 'u=1, i',
    "referer": "https://www.iplace.com.br/buyback-serial",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}


def getData(imei):
    data = r'{"url":"/buyback/aquisicao/elegibilidade/dispositivo/359888171995975","data":{},"method":"GET"}'

    res = post(url=url, data=data, headers=headers, timeout=10)

    print(res.status_code)

    if res.ok:
        resjoin = res.json()
        response = {
            "code": 200,
            "describe": "",
            "data": {
                "IMEI/SN": str(imei),
                "设备型号": resjoin.get("aparelho"),
                "容量": resjoin.get("capacidade"),
                "颜色": resjoin.get("cor"),
            }
        }
    else:
        response = {
            "code": 500,
            "describe": "request is error",
            "data": {}
        }

    return response

