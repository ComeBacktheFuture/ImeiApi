import requests
from bs4 import BeautifulSoup

headers = {
	'Host':'one.andro.plus',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	'Origin':'https://one.andro.plus',
	'Referer':'https://one.andro.plus/region.php',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9',
}

url = "https://one.andro.plus/reg.php"


def getData(imei):
	data = f"target_code={imei}"

	try:
		res = requests.post(url, headers=headers, data=data, timeout=10)
	except Exception as e:
		return {
			"code": 500,
			"describe": "request is error",
			"data": {}
		}

	if res.ok:
		r = BeautifulSoup(res.text, "lxml").find(name="p")

		if r is None:
			response = {
				"code": 500, 
				"describe": "can't find data", 
				"data": {}
			}

		text = r.get_text()

		if len(text.split(":")) < 2:
			response = {
				"code": 500, 
				"describe": "can't find data", 
				"data": {}
			}

		code = text.split(":")[-1]

		response = {
			"code": 200, 
			"describe": "", 
			"data": {
				"Unlock code is": code,
			}
		}
	else:
		response = {
			"code": res.status_code,
			"describe": "request is error",
			"data": {}
		}

	return response



if __name__ == '__main__':
	print(getData("869128053706080"))

