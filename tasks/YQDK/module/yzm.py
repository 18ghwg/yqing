# -*- coding: utf-8 -*-
"""
@Time    : 2022/12/16 11:30
@Author  : ghwg
@File    : get_move_end_x.py
滑块验证码处理函数
"""
import base64
import cv2
import httpx
import numpy as np
from module.mysql.WebClass import web_class


# 获取验证码信息
async def get_yzm(client: httpx.AsyncClient):
    api_url = web_class.get_web_config()["DKURL"] + '/student/website/verify/image'
    res = (await client.get(api_url)).json()
    await client.aclose()
    return {"SrcImage": res.get("SrcImage"), "YPosition": res.get("YPosition")}


# 处理base64图片
async def mod_base64(base64_code):
    # base64解码
    img_data = base64.b64decode(base64_code)
    # 转换为np数组
    img_array = np.fromstring(img_data, np.uint8)
    # 转换成opencv可用格式
    img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    return img


# 处理滑块验证码X坐标
async def get_move_end_x(YPosition: int, SrcImage: str):
    blue = 192
    green = 192
    red = 192
    img = await mod_base64(SrcImage)  # 处理图片
    img = cv2.resize(img, (280, 158), interpolation=cv2.INTER_CUBIC)  # 指定图片大小
    x, y, z = img.shape
    XPosition = 0  # x坐标
    for XPosition in range(y):
        if img[YPosition, XPosition, 0] == blue & \
                img[YPosition, XPosition, 1] == green & \
                img[YPosition, XPosition, 1] == red:
            break
        else:
            continue
    return XPosition


# 滑块验证
async def yzm(client: httpx.AsyncClient):
    """
    @param client: 异步线程
    @param moveEnd_X: 滑块正确的x坐标
    @return: True: 验证成功 False: 验证失败
    """
    """处理滑块验证码信息"""
    yzm_json = await get_yzm(client)  # 获取验证码信息：得到验证码图片地址和Y坐标
    moveEnd_X = await get_move_end_x(yzm_json["YPosition"], yzm_json["SrcImage"])
    """滑块请求"""
    api_url = web_class.get_web_config()["DKURL"] + '/student/website/verify/image/result'
    data = {
        "moveEnd_X": moveEnd_X,
        "wbili": 0.9333333333333333
    }
    res = (await client.post(api_url, data=data)).text
    print(res)
    if res == 'fail':
        return False
    else:
        return True


