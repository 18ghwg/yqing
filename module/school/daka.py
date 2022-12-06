# -*- coding: utf-8 -*-
"""
@Time    : 2022/11/12 9:49
@Author  : ghwg
@File    : daka.py

"""


# 检查账号密码有效性
import json

import requests

from config import logger
from module.base import jiami
from module.mysql.UserClass import user_class
from module.mysql.WebClass import web_class
from module.school.session import session


def check_user(xuehao: str, password: str):
    """
    :param xuehao: 学号
    :param password: 密码
    :return: True：登陆成功  String：登陆失败  超时：学校服务器关闭
    """
    url = f'{web_class.get_web_config()["DKURL"]}/student/website/login'

    data = {
        'uname': xuehao,
        'pd_mm': jiami(password)
    }
    try:
        response = session.post(url=url, data=data, timeout=3)
        sc = response.json()
        if "msg" in str(sc):  # 登录出错
            return sc.get('msg')
        else:  # 登录成功
            if len(str(xuehao)) < 10:
                user_class.add_not_student_user(xuehao, password)  # 记录非学生账号到表中
                return False
            else:
                return True
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException):
        return "超时"
    except json.decoder.JSONDecodeError:
        return "超时"


# 判断历史打卡信息
def get_last_info() -> int:
    """
    :return: 1：获取到历史打卡信息  0：历史打卡信息为空
    """
    try:
        res = session.get(url=f'{web_class.get_web_config()["DKURL"]}/student/content/student/temp/zzdk/lastone')
        logger.debug("用户历史打卡信息不为空！")
        return 1
    except Exception as e:
        logger.info("用户历史打卡信息为空！")
        logger.error(e)
        return 0


# 获取打卡记录
def get_home_zzdk_info(xuehao: str):
    check_data = check_user(xuehao, user_class.get_user_password(xuehao))
    if check_data is True:
        api_url = f'{web_class.get_web_config()["DKURL"]}/student/content/tabledata/student/temp/zzdk?bSortable_0=false&bSortable_1=true&iSortingCols=1&iDisplayStart=0&iDisplayLength=12&iSortCol_0=1&sSortDir_0=desc'
        try:
            res = session.get(api_url)
        except requests.Timeout:
            return None
        else:
            return json.loads(res.text)
    else:
        return None







