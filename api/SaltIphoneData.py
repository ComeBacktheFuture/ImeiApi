
from PIL import Image
import numpy as np
from io import BytesIO

import requests
import ddddocr
import pytesseract

from bs4 import BeautifulSoup
from pprint import pprint


ocr = ddddocr.DdddOcr()
ocr.set_ranges(6)

headers = {
	"Proxy-Connection": "keep-alive",
	"X-Requested-With": "XMLHttpRequest",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
	"Accept": "text/html, */*; q=0.01",
	"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "zh-CN,zh;q=0.9",
}


def to_init(path):
    img = Image.open(path)
    return img


def to_gary(img: Image):
    """
    灰度化
    :param img: 图像
    :return: 灰度化图像
    """
    gary = img.convert("L")
    return gary


def noise_reduction(img: Image, g, n=5):
    """"""
    row, col = img.width, img.height

    for r in range(g):
        for x in range(row):
            for y in range(col):
                if x == 0 or y == 0 or x >= row-2 or y >= col-2:
                    img.putpixel((x, y), 1)
                    continue

                sum = img.getpixel((x - 1, y - 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1)) \
                      + img.getpixel((x, y - 1)) \
                      + img.getpixel((x, y)) \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y - 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))

                if 0 < (9 - sum) < n and (img.getpixel((x, y)) == 0):
                    img.putpixel((x, y), 1)

    return img


def to_binary(img: Image, threshold=180):
    table = list()
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    img_binary = img.point(table, '1')
    return img_binary


def to_fix(img: Image, n=4):
    row, col = img.width, img.height

    for x in range(row):
        for y in range(col):
            if x == 0 or y == 0 or x >= row-2 or y >= col-2:
                continue
            if img.getpixel((x, y)) == 1:
                sum = img.getpixel((x - 1, y - 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1)) \
                      + img.getpixel((x, y - 1)) \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y - 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))
                if 0 <= sum < n:
                    img.putpixel((x, y), 0)

    return img


def print_img(img: Image):
    row, col = img.width, img.height

    for y in range(col-1):
        for x in range(row-1):
            if img.getpixel((x, y)) == 1:
                print(" ", end="")
            else:
                print("0", end="")
        print()


def num_letter_security_code_recognition(image):
    img = to_init(BytesIO(image))
    img = to_gary(img)
    img = to_binary(img)
    img = noise_reduction(img, g=6, n=5)
    img = to_fix(img, 4)
    text = ocr.classification(img)
    text_list = list()
    n = 0
    while n < len(text):
        if n == 0:
            text_list.append(text[n])
            if text[n].isalpha():
                text_list.append(text[n].upper())
        else:
            if text[n].isalpha():
                _ = list()
                s = 0
                while s < len(text_list):
                    _.append(text_list[s] + text[n].upper())
                    text_list[s] += text[n]
                    s += 1
                text_list += _
            else:
                s = 0
                while s < len(text_list):
                    text_list[s] += text[n]
                    s += 1
        n += 1
    return text_list


def getData(imei):
	session = requests.Session()
	session.headers = headers

	# get cookies
	_ = session.get("https://www.salt.ch/en")
	# assert _.ok, f"init1界面出現問題: {_.status_code}"
	_ = session.get("https://www.salt.ch/en/options-services/upgrade-repair/repair")
	# assert _.ok, f"init2界面出現問題: {_.status_code}"
	_ = session.get("http://repair.salt.ch/External/Action/27427839-ade1-46ad-ab14-e03bcdf4b5b4")
	# assert _.ok, f"init3界面出現問題: {_.status_code}"
	_ = session.get("http://repair.salt.ch/CaseWizard/Salt/27427839-ade1-46ad-ab14-e03bcdf4b5b4/New")
	# assert _.ok, f"init4界面出現問題: {_.status_code}"

	# connect first url
	_ = session.get("http://repair.salt.ch/CaseWizard/Salt/27427839-ade1-46ad-ab14-e03bcdf4b5b4")
	# assert _.ok, f"first界面出現問題: {_.status_code}"
	token = k['value'] if (k:=BeautifulSoup(_.text, "lxml").find(name="input", attrs={"name": "__RequestVerificationToken"})) is not None else None

	data = f"__RequestVerificationToken={token}&SelectedAnswers%5B0%5D=0"

	# connect Se url
	_ = session.post("http://repair.salt.ch/CaseWizard/StepSaltInsuranceRepairAtHome/EditStep", data=data)
	# assert _.ok, f"Se界面出現問題: {_.status_code}"

	# connect Th url
	_ = session.post("http://repair.salt.ch/CaseWizard/StepSaltProduct/RenderStep")
	# assert _.ok, f"Th界面出現問題: {_.status_code}"
	bsh = BeautifulSoup(_.text, "lxml")
	token = k['value'] if (k:=bsh.find(name="input", attrs={"name": "__RequestVerificationToken"})) is not None else None
	image = k['src'] if (k:=bsh.find(name="img", attrs={"alt": "captcha"})) is not None else None

	# vir image code
	c = False
	while c is False:
		_ = session.get(f"http://repair.salt.ch/{image}")
		assert _.ok, f"image界面出現問題: {_.status_code}"
		text_list = num_letter_security_code_recognition(_.content)
		for text in text_list:
			c = session.post("http://repair.salt.ch/CaseWizard/StepSaltProduct/ValidateCaptcha", data=f"captcha={text}").json()['captcha']
			if c is True:
				break


	data = f"__RequestVerificationToken={token}" \
		   f"&SerialNumber={imei}" \
		   f"&ProductName=Apple+-+iPhone+13+128GB+%E8%93%9D%E8%89%B2" \
		   f"&ProductId=19050887&ManufacturerBusinessunitId=0&CaptchaString={text}&confirm=Next"


    # connect this url
	_ = session.post(url="http://repair.salt.ch/CaseWizard/StepSaltProduct/EditStep", data=data)
	# assert _.ok, f"this界面出現問題: {_.status_code}"

	res = _.text.replace("<br />", "\n")
	bsh = BeautifulSoup(res, "lxml")
	content = e.get_text() if (e:=bsh.find(id="dialog_fmip")) is not None else None

	if content is None:
		return {
			"code": 400, 
			"describe": "未找到数据", 
			"data": {
				"primary data": _.text
			}
		}

	content_list = content.split("\n")

	find = None
	iCloudStatus = None
	for i in content_list:
		if "Find" in i:
			result = content[content.index(i)+1]
			if "yes" in result:
				find = True
			elif "no" in result:
				find = False

		if "Lost" in i:
			result = content[content.index(i)+1]
			if "yes" in result:
				iCloudStatus = True
			elif "no" in result:
				iCloudStatus = False

	response = {
		"code": 200, 
		"describe": "", 
		"data": {
			"IMEI": imei, 
			"Model": "Apple - iPhone 13 128GB 蓝色", 
			"Find My IPhone": "ON" if find is True else "OFF", 
			"iCloudStatus": "Cle an" if iCloudStatus is False else "Lost"
		}
	}

	return response




