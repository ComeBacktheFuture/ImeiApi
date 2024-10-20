# ImeiApi

## api接口

### ``GET`` ``/api/iphone_data`` 返回手机型号，容量，颜色

参数
- ``type``: 指定返回数据类型
  - ``json``
  - ``txt``
- ``imei``: 指定所查找的手机的imei

状态码
- ``200``: 正常访问
- ``500``: 服务器未能获得所查找的数据

txt形式返回数据示例

```http://127.0.0.1:10000/api/iphone_data?imei=359888171995975&type=txt```

```bazaar
IMEI/SN: 359888171995975
设备型号: iPhone 13
容量: 128GB
颜色: Rosa
```

###  ``GET`` ``/api/iphone_unlock_code`` 返回手机型号，容量，颜色

参数
- ``type``: 指定返回数据类型
  - ``json``
  - ``txt``
- ``imei``: 指定所查找的手机的imei

状态码
- ``200``: 正常访问
- ``500``: 服务器未能获得所查找的数据

txt形式返回数据示例

```/api/iphone_unlock_code?type=text&imei=869128053706080```

```
Unlock code is: 1aa5629f7b3d6f9c
```

