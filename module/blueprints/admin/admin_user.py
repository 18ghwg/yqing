# -*- coding: utf-8 -*-
"""
@Time    : 2022/10/25 22:11
@Author  : ghwg
@File    : admin_user.py

"""
from flask import Blueprint, request, render_template
from exts import limiter
from module.blueprints.admin import admin_login_check
from module.mod_post_requests import mod_post_data_info
from module.mysql.AdminClass import admin_class
from module.mysql.UserClass import user_class

admin_user_bp = Blueprint("admin_user", __name__, url_prefix="/admin")


# 用户列表
@admin_user_bp.route("/UserInfo", methods=["GET"])
@limiter.exempt()
@admin_login_check
def user_list():
    # 获取参数
    try:
        pag = int(request.args.get("pag", default=1))
    except TypeError:
        # 搜索的学号
        xuehao = request.args.get("xuehao")
        _list = user_class.admin_search_user(xuehao)
        user_num = len(_list)  # 用户数量
        pag_num = admin_class.mod_pag(user_num)  # 处理pag页数
        info = {
            "user_list": _list,
            "user_num": user_num,
            "pag_num": pag_num,
            "pag_list": [1],
            "pag_now": 0,

        }
    else:
        _list = user_class.get_user_list()  # 用户列表
        user_num = len(_list)  # 用户数量
        pag_num = admin_class.mod_pag(user_num)  # 处理pag页数
        info = {
            "user_list": _list[pag * 50 - 50:pag * 50],
            "user_num": user_num,
            "pag_num": pag_num,
            "pag_list": [pag + 1 for pag in range(pag_num)],
            "pag_now": pag,

        }
    return render_template("admin/info/user/user-list.html", **info)


# 删除用户
@admin_user_bp.route("/user/del", methods=["POST"])
@limiter.exempt()
@admin_login_check
def user_del():
    _data = mod_post_data_info()
    try:
        xuehao = _data["xuehao"]
    except KeyError:
        return {"code": 500, "msg": "参数有误"}
    else:
        # 删除请假信息
        _del_data = user_class.deluser(xuehao, "admin删除")
        if _del_data:
            return {"code": 200, "msg": f"{xuehao}已删除"}
        else:
            return {"code": 400, "msg": "删除失败"}


# 更新用户信息
@admin_user_bp.route("/UserInfo/Put", methods=["POST"])
@limiter.exempt()
@admin_login_check
def user_put_info():
    _data = mod_post_data_info()  # 获取请求信息
    try:
        xuehao = _data["xuehao"]
        password = _data["password"]
        email = _data["email"]
        room_num = _data["room_num"]
        credit = int(_data["credit"])
        qqh = _data["qqh"]
        state = int(_data["state"])
        dk_time = _data["dk_time"]
        check_state = int(_data["check_state"])
    except KeyError:
        return {"code": 500, "msg": "参数有误"}
    else:
        info = {
            "xuehao": xuehao,
            "password": password,
            "email": email,
            "qqh": qqh,
            "room_num": room_num,
            "state": state,
            "check_state": check_state,
            "dk_time": dk_time,
            "credit": credit,
                }

        return user_class.put_user_info(info)


# 黑名单列表
@admin_user_bp.route("/BlackList", methods=["GET"])
@limiter.exempt()
@admin_login_check
def black_list():
    # 获取参数
    pag = int(request.args.get("pag", default=1))
    _list = user_class.get_black_list()  # 黑名单列表
    black_num = len(_list)  # 黑名单数量
    pag_num = admin_class.mod_pag(black_num)  # 处理pag页数
    info = {
        "black_list": _list[pag * 50 - 50:pag * 50],
        "black_num": black_num,
        "pag_num": pag_num,
        "pag_list": [pag + 1 for pag in range(pag_num)],
        "pag_now": pag,

    }
    return render_template("admin/info/user/black-list.html", **info)


# 删除黑名单
@admin_user_bp.route("/black/del", methods=["POST"])
@limiter.exempt()
@admin_login_check
def del_black():
    _data = mod_post_data_info()
    try:
        xuehao = _data["xuehao"]
    except KeyError:
        return {"code": 500, "msg": "参数有误"}
    else:
        # 删除请假信息
        _del_data = user_class.delblack(xuehao)
        if _del_data:
            return {"code": 200, "msg": f"{xuehao}已删除"}
        else:
            return {"code": 400, "msg": "删除失败"}





