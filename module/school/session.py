# -*- coding: utf-8 -*-
"""
@Time    : 2022/11/12 9:51
@Author  : ghwg
@File    : session.py

"""
import requests


session = requests.session()  # 实体化函数
session.headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}
