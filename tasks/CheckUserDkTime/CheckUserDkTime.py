# -*- coding: utf-8 -*-
"""
@Time    : 2022/11/30 8:54
@Author  : ghwg
@File    : CheckUserDkTime.py
检查用户打卡时间并修改到人数少的打卡时间
"""
from config import logger
from exts import app
from module.mysql import UsersList
from module.mysql.UserClass import user_class


def check_user_dk_time():
    # 获取用户列表
    with app.app_context():
        user_list_all = UsersList.query.filter_by().all()
        logger.info("【检测用户打卡时间】开始")
        for user in user_list_all:  # 遍历每个用户
            xuehao = user.xuehao  # 学号
            dk_time = user.dk_time  # 打卡时间
            with app.app_context():
                if user_class.get_dk_time_user_num(dk_time) > 50:  # 同一时间的打卡人数大于50人 -> 修改打卡时间
                    logger.info(f"【检测用户打卡时间】{xuehao}统一打卡时间的人数已超50人，现在开始更改用户打卡时间")
                    with app.app_context():
                        if not user_class.mod_dk_time(xuehao, dk_time):  # 修改用户打卡时间到人数较少的时间 -> 失败
                            logger.info("【检测用户打卡时间】修改失败：用户不存在")
        logger.info("【检测用户打卡时间】结束")



