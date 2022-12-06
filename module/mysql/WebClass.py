# -*- coding: utf-8 -*-
"""
@Time    : 2022/10/26 8:57
@Author  : ghwg
@File    : WebClass.py

"""
from exts import db, app
from module.mysql import Config
from module.mysql.modus import get_sql_info


class WebClass:

    # 读取网站配置
    @classmethod
    def get_web_config(cls):
        # 读取配置信息->dict
        with app.app_context():
            sql_info = get_sql_info(Config)
            if sql_info:
                sql_info["managerlist"] = [int(i) for i in str(sql_info['Managers']).split(',')]
                sql_info["Groups"] = [int(i) for i in str(sql_info['Groups']).split(',')]
                return sql_info
            else:
                return False


web_class = WebClass()

