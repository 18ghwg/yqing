# -*- coding: utf-8 -*-
"""
@Time    : 2022/11/12 9:53
@Author  : ghwg
@File    : info.py

"""

# 获取宿舍号
import json
import re
from typing import Union

import requests

from config import logger
from module import sendwxbot
from module.base import jiami
from module.mysql.UserClass import user_class
from module.mysql.WebClass import web_class
from module.school.daka import check_user, get_last_info
from module.school.session import session


# 获取宿舍号码
def get_room_num(xuehao, password):
    session_two = requests.session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 11; zh-cn; MI 9 Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.116 Mobile Safari/537.36 XiaoMi/MiuiBrowser/16.2.25 swan-mibrowser",
    }
    session_two.headers.update(headers)
    _data = {
        "uname": xuehao,
        "pd_mm": jiami(password),
    }
    try:
        session_two.post("https://xgyyx.njpi.edu.cn/website/login", data=_data, timeout=3)  # 登录迎新平台
        res = session_two.get("https://xgyyx.njpi.edu.cn/wap/menu/stu/welcome/xxcx", timeout=3)
        building = re.findall('id:"ssxx_lf",label:"宿舍楼",text:"(.*?)"', res.text)[0]
        room_num = re.findall('id:"ssxx_fj",label:"宿舍",text:"(.*?)"', res.text)[0]
        if building == "山畔综合楼":
            room_num = building + room_num
    except:
        room_num = None
    return room_num


# 获取信息
def hq_webinfo(xuehao: str, password: str):
    """
    :param xuehao: 学号
    :param password: 密码
    :return: 超时：登录超时、False：登录失败、dict：用户信息
    """
    try:
        check_data = check_user(xuehao, password)
        if check_data is True:
            res = session.get(url=web_class.get_web_config()["DKURL"] + '/student/content/student/self/info',
                              timeout=3)
            name = res.json()['xm']  # 姓名
            gender = res.json()['xb']['mc']  # 性别：男性/女性
            clas = res.json()['szbj']['bjmc']  # 班级
            xhXm = res.json()['xhXm']  # [学号]姓名
            qqh = res.json()['qqh']  # QQ
            room_num = get_room_num(xuehao, password)  # 宿舍号
            dk_info = get_last_info()  # 打卡信息状态
            return {"name": name, "gender": gender, "clas": clas, "xhXm": xhXm,
                    "qqh": qqh, "room_num": room_num, "dk_info": dk_info}
        elif "超时" in check_data:  # 登陆超时
            return "超时"
        else:  # 登录失败
            return False
    except Exception as e:
        sendwxbot("疫情打卡网站：\n获取用户信息出错！\n请管理员查看日志！")
        logger.info(e)
        return {"name": None, "gender": None, "clas": None, "xhXm": None,
                "qqh": None, "dk_info": None}


# 获取接口json配置
def get_home_json(url: str) -> Union[None, dict]:
    try:
        api_url = url
        res = session.get(f'{web_class.get_web_config()["DKURL"]}{api_url}', timeout=3)
    except requests.Timeout:
        return None
    else:
        return json.loads(res.text)


# 获取用户json信息
def get_user_json_info(xuehao: str, url: str) -> Union[dict, None, str]:
    password = user_class.get_user_password(xuehao)  # 获取密码
    if password:
        check_data = check_user(xuehao, password)
        if check_data is True:
            try:
                api_url = f'{web_class.get_web_config()["DKURL"]}{url}'
                res = session.get(api_url, timeout=3)
            except requests.Timeout:
                return ""
            else:
                if res.text == "":  # 信息为空
                    return ""
                else:
                    return res.json()
        else:
            return ""
    else:
        return ""


# 正则获取网页字符
def get_home_web_str(xuehao: str, api_url: str, key: str):
    """
    :param xuehao: 学号
    :param api_url: api链接
    :param key: 正则内容
    :return:
    """
    password = user_class.get_user_password(xuehao)  # 获取密码
    if password:
        check_data = check_user(xuehao, password)
        if check_data is True:
            try:
                res = session.get(f'{web_class.get_web_config()["DKURL"]}{api_url}')
            except requests.Timeout:
                return ""
            else:
                try:
                    str_value = re.findall(key, res.text)[0]
                except IndexError:
                    return ""
                else:
                    return str_value
        else:
            return ""
    else:
        return ""


