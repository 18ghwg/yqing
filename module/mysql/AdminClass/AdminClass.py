# -*- coding: utf-8 -*-
"""
@Time    : 2022/10/23 14:32
@Author  : ghwg
@File    : AdminClass.py

"""
import asyncio

from module.mysql.UserClass import user_class
from module.mysql.models import Admins


class Admin:
    # 账号密码检测
    @classmethod
    def check_admin_password(cls, xuehao: str, password: str):
        admin_data = Admins.query.filter_by(xuehao=xuehao, password=password).first()
        if admin_data:  # 账号密码正确
            return True
        else:
            return False

    # 管理员后台获取网站信息
    @classmethod
    def get_admin_web_info(cls):
        user_num = user_class.get_user_num()  # 使用人数
        user_today = user_class.get_user_new_today()  # 今日账号新增
        user_week_info = asyncio.run(user_class.get_user_week_num())  # 获取七日账号新增
        web_info = {
            "user": {
                "user_num": user_num,
                "user_today": user_today,
                "user_week_list": user_week_info["week"],
                "user_week_num": user_week_info["num"],
            }
        }
        return web_info

    # 分页处理
    @classmethod
    def mod_pag(cls, num: int) -> int:
        pag_max = num / 50
        # 不满足分页条件的数据单独创建一个分页
        if int(str(pag_max).split('.')[1]) != 0:  # 含有小数
            pag_max = int(pag_max) + 1
        else:
            pag_max = int(pag_max)
        return pag_max


# 实例化类
admin_class = Admin()
