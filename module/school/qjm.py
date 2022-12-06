# -*- coding: utf-8 -*-
"""
@Time    : 2022/12/4 16:00
@Author  : ghwg
@File    : qjm.py
操作请假申请、请假码
"""
from module.mysql.WebClass import web_class
from module.school.daka import check_user
from module.school.session import session


# 提交请假申请
def up_qj_apply(xuehao: str, password: str):
    """
    :param xuehao: 学号
    :param password: 密码
    :return:
    """
    api_url = f'{web_class.get_web_config()["DKURL"]}/student/content/student/leave/apply_stu'
    login_data = check_user(xuehao, password)  # 登录账号
    if login_data:  # 登录成功
        data = {
            "qjlxM.dm": 1,
            "qjlx": "私事假",
            "kssj": "2022-12-05 15:41",
            "jssj": "2022-12-05 18:00",
            "ts": 0,
            "jsTs": 0,
            "hour": 3,
            "jsHour": 3,
            "qjsy": "买东西",
            "lxr": "妈妈",
            "lxrdh": 18361487965,
            "lxInd": 1,
            "lxqx.dm": "320000,320100,320116",
            "lxqx1": "江苏省/南京市/六合区",
            "lxMdd": "门口",
            "huisusheInd": 0,
            "lxBz": 7219,
            "chushiInd": 0,
            "chushengInd": 0,
            "pathFile": "",
            "qjLocation": "江苏省南京市六合区大厂街道欣乐路124号欣乐新村",
            "qjLocationZb": "118.751885,32.233441",
            "operationType": "Create",
            "id": "",
        }
        res = session.post(api_url, data=data)
        print(res.text)
        return True
    else:  # 登录失败
        print("登录失败")
        return False
