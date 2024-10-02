# -*- coding = utf-8 -*-
# @Time : 2024/10/1 0001 23:10
# @Author : SleepCat
# @File : iphoneData.py
# @Software : PyCharm


from requests import post
from googletrans import Translator

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

translater = Translator()

def getData(imei):
    data = r'{"url":"/buyback/aquisicao/elegibilidade/dispositivo/'+str(imei)+'","data":{},"method":"GET"}'

    try:
        res = post(url=url, data=data, headers=headers, timeout=10)
    except Exception as e:
        return {
            "code": 500,
            "describe": "request is error",
            "data": {}
        }

    if res.ok:
        resjoin = res.json()

        color = resjoin.get("cor")
        if color == "Branco":
            color = "White"
        elif color == "Roxo":
            color = "Purple"
        elif color == "Preto":
            color = "Black"
        elif color == "Titânio":
            color = "Titanium"
        elif color == "Estelar":
            color = "Starlight"
        elif color =="Cinza Espacial":
            color = "Space Gray"
        elif color =="Dourado":
            color = "Gold"
        elif color == "Grafite":
            color = "Graphite"
        elif color == "Vermelho":
            color = "Red"
        elif color == "Azul":
            color = "Blue"
        elif color == "Azul Pacífico":
            color = "Pacific Blue"
        elif color == "Roxo-Profundo":
            color = "Deep Purple"
        elif color == "Preto-Espacial":
            color = "Space Black"
        elif color == "Meia-Noite":
            color = "Midnight"
        elif color == "Titânio Branco":
            color = "White Titanium"
        elif color == "Verde Meia-Noite":
            color = "Midnight Green"
        elif color == "Titânio Preto":
            color = "Black Titanium"
        elif color == "Prateado":
            color = "Silver"
        elif color == "Azul-Sierra":
            color = "Blue Sierra"
        elif color == "Verde Alpino":
            color = "Alpine Green"
        elif color == "Rosa":
            color = "Pink"
        else:
            color = translater.translate(color, src="es", dest="en").text

        response = {
            "code": 200,
            "describe": "",
            "data": {
                "IMEI/SN": str(imei),
                "设备型号": resjoin.get("aparelho"),
                "容量": resjoin.get("capacidade"),
                "颜色": color,
            }
        }
    else:
        response = {
            "code": 500,
            "describe": "request is error",
            "data": {}
        }

    return response

