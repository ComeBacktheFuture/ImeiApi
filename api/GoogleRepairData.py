#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import time
import execjs
from pprint import pformat
from DrissionPage import Chromium

from DrissionPage import ChromiumOptions


opt = ChromiumOptions(read_file=False)

if sys.platform.startswith('linux'):
    opt.set_browser_path('/opt/google/chrome/google-chrome')  # 设置路径
opt.no_imgs(True).mute(True)  # 不加载图片 并 静音
opt.incognito()  # 匿名模式
# opt.headless()  # 无头模式
opt.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36')
# opt.set_argument('--no-sandbox')  # 无沙盒模式

tab = Chromium(addr_or_opts=opt).latest_tab


login_url = r'https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fstore.google.com%2Fus%2Frepair%3Fhl%3Den-US%26pli%3D1&hl=en-US&faa=1&ddm=0&flowName=GlifWebSignIn&flowEntry=AccountChooser'
repair_url = r'https://store.google.com/us/repair?hl=en-US'
port_point = "/data/batchexecute?rpcids=VEV8Hf"


def login(assount: str, password: str):
	# 登录
	tab.get(login_url)

	assount_input = tab.ele("#identifierId")
	assount_input.input(assount+"\n", clear=True)

	time.sleep(3)

	password_input = tab.ele("@type=password")
	password_input.input(password+"\n", clear=True)

	time.sleep(5)

	# 未成功登录检测
	if "us/repair" not in tab.url or (not tab.url_available):
		raise Exception(f"账号{assount}登录失败...")

	print(f"账号{assount}登录成功...")



def getData(imei: str):
	# 获取数据
	tab.get(repair_url)

	tab.listen.start(port_point)

	_input = tab.ele("@tag()=input")
	_input.input(imei+"\n", clear=True)

	while (res:=tab.listen.wait(timeout=1, raise_err=False)) is False:
		time.sleep(0.01)

	text = res.response.body

	text_list = text.split("\n")

	cen_content = execjs.eval(text_list[3].replace("\\", "").replace('"[', '[').replace(']"', ']'))
	ex_content = execjs.eval(text_list[5].replace("\\", "").replace('"[', '[').replace(']"', ']'))


	Model_Name = Description = cen_content[0][2][1][1][2]
	Model_SKU = cen_content[0][2][1][1][1]
	Model_Code = None
	Serial = cen_content[0][2][1][0][0][1]
	IMEI1 = cen_content[0][2][1][0][1][1]
	IMEI2 = cen_content[0][2][1][0][2][1]
	ESIM_ID = cen_content[0][2][1][0][3][1]
	Purchase_Country = None
	Intended_Region = None
	Activation_Status = bool(cen_content[0][2][1][-2][-1] and cen_content[0][2][1][-2][-2])
	Warranty_Status = bool(cen_content[0][2][1][-1])
	Warranty_Start_Date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cen_content[0][2][1][-2][0][0][0]))
	Warranty_End_Date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cen_content[0][2][1][-2][0][1][0]))
	Device_Age = cen_content[0][2][1][-2][1]

	response = {
        "code": 200,
        "describe": "",
        "data": {
        	"Model Name": Model_Name, 
        	"Model SKU": Model_SKU, 
        	"Serial": Serial, 
        	"IMEI1": IMEI1, 
        	"IMEI2": IMEI2, 
        	"ESIM ID": ESIM_ID, 
        	"Activation Status": "Not previously activated" if Activation_Status is True else "Activated", 
        	"Warranty Status": "Expired" if Warranty_Status is False else "Not Expired",
        	"Warranty Start Date": Warranty_Start_Date,
        	"Warranty End Date": Warranty_End_Date, 
        	"Device Age": str(Device_Age), 
        	"primary data": "\n" + pformat(cen_content[0]) + "\n" + pformat(ex_content[0])
        }
	}

	return response

