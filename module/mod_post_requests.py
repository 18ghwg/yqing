# -*- coding: utf-8 -*-
"""
@Time    : 2022/10/23 18:17
@Author  : ghwg
@File    : mod_post_requests.py

"""
# 处理post信息
from urllib.parse import unquote

from flask import request


def mod_post_data_info():
    data = request.get_data()
    text = data.decode("utf-8")
    sp = text.split("&")
    i = 0
    kv = {}
    for s in sp:
        # print("{} s = {}".format(i, s))
        pp = s.split("=")
        if len(pp) == 2:
            value = pp[1]
            kv[pp[0]] = unquote(value)
    return kv
