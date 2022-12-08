# -*- coding: utf-8 -*-
"""
@Time    : 2022/10/25 13:10
@Author  : ghwg
@File    : admin_credit.py

"""
from flask import request, render_template, Blueprint
from exts import limiter
from module.blueprints.admin import admin_login_check
from module.mod_post_requests import mod_post_data_info
from module.mysql import CreditConfig
from module.mysql.AdminClass import admin_class
from module.mysql.CreditClass import credit_class
from module.mysql.modus import get_sql_info, put_sql_info

admin_credit_bp = Blueprint("admin_credit", __name__, url_prefix="/admin")


# 积分配置
@admin_credit_bp.route("/CreditInfo", methods=["POST", "GET"])
@limiter.exempt()
@admin_login_check
def credit_info():
    if request.method == "GET":
        # 获取积分配置
        info = get_sql_info(CreditConfig)
        return render_template("admin/info/credit/credit-info.html", **info)
    else:
        kv = mod_post_data_info()  # 获取请求信息
        try:
            QJMCredit = kv["QJMCredit"]  # 请假码消耗积分数量
            CheckCredit = kv["CheckCredit"]  # 签到获得积分数量
            JoinCredit = kv["JoinCredit"]  # 新用户赠送积分
        except KeyError:
            return {"code": 500, "msg": "参数有误"}
        else:
            # 更新配置
            sql_data = {
                "CheckCredit": CheckCredit,
                "QJMCredit": QJMCredit,
                "JoinCredit": JoinCredit,
            }
            put_sql_info(CreditConfig, sql_data)
            return {"code": 200, "msg": "积分配置更新成功"}


# 积分使用记录列表
@admin_credit_bp.route("/CreditUseList", methods=["POST", "GET"])
@limiter.exempt()
@admin_login_check
def credit_log_list():
    # 获取get参数
    try:
        pag = request.args.get("pag", default=1, type=int)  # 页码
    except TypeError:
        xuehao = request.args.get("xuehao")  # 学号
        _list = credit_class.admin_search_credit_info(xuehao)  # log列表
        log_num = len(_list)  # 请假码数量
        pag_num = admin_class.mod_pag(log_num)  # 处理pag页数
        info = {
            "log_list": _list,
            "log_num": log_num,
            "pag_num": pag_num,
            "pag_list": [pag + 1 for pag in range(pag_num)],
            "pag_now": 0,

        }
    else:
        _list = credit_class.get_credit_log_list()  # log列表
        log_num = len(_list)  # 请假码数量
        pag_num = admin_class.mod_pag(log_num)  # 处理pag页数
        info = {
            "log_list": _list[pag * 50 - 50:pag * 50],
            "log_num": log_num,
            "pag_num": pag_num,
            "pag_list": [pag + 1 for pag in range(pag_num)],
            "pag_now": pag,

        }
    return render_template("admin/info/credit/credit-list.html", **info)


# 删除积分记录
@admin_credit_bp.route("/credit/del", methods=["POST"])
@limiter.exempt()
@admin_login_check
def credit_del():
    _data = mod_post_data_info()
    try:
        xuehao = _data["xuehao"]  # 学号
        time = _data["time"]  # 记录时间
    except KeyError:
        return {"code": 500, "msg": "参数有误"}
    else:
        # 删除请假信息
        _del_data = credit_class.del_credit_log({"xuehao": xuehao, "time": time})
        if _del_data:
            return {"code": 200, "msg": f"{xuehao}的积分记录已删除"}
        else:
            return {"code": 400, "msg": "删除积分记录失败"}


# 积分活动配置
@admin_credit_bp.route("/CreditActivity", methods=["POST", "GET"])
@limiter.exempt()
@admin_login_check
def credit_activit():
    if request.method == "GET":
        info = get_sql_info(CreditConfig)
        return render_template("admin/info/credit/credit-activity.html", **info)
    else:
        # 获取post配置
        post_data = mod_post_data_info()
        try:
            ActivityUserGetNum = post_data["ActivityUserGetNum"]  # 请假码消耗积分数量
            ActivityAdminGetNum = post_data["ActivityAdminGetNum"]  # 签到获得积分数量
            ActivityStartTime = post_data["ActivityStartTime"]  # 新用户赠送积分
            ActivityEndTime = post_data["ActivityEndTime"]  # 新用户赠送积分
        except KeyError:
            return {"code": 500, "msg": "参数有误"}
        else:
            # 更新配置
            sql_data = {
                "ActivityUserGetNum": ActivityUserGetNum,
                "ActivityAdminGetNum": ActivityAdminGetNum,
                "ActivityStartTime": ActivityStartTime,
                "ActivityEndTime": ActivityEndTime,
            }
            put_sql_info(CreditConfig, sql_data)
            return {"code": 200, "msg": "积分配置更新成功"}


# 积分活动json配置接口
@admin_credit_bp.route("/credit/config", methods=["GET"])
@limiter.exempt()
def credit_config():
    info = get_sql_info(CreditConfig)
    if info:
        user_get_num = info["ActivityUserGetNum"]
        admin_get_num = info["ActivityAdminGetNum"]
        start_time = str(info["ActivityStartTime"])
        end_time = str(info["ActivityEndTime"])
        return {
            "code": 200,
            "user_get_num": user_get_num,
            "admin_get_num": admin_get_num,
            "start_time": start_time,
            "end_time": end_time,
        }
    else:  # 配置获取失败
        return {
            "code": 400,
            "user_get_num": "",
            "admin_get_num": "",
            "start_time": "",
            "end_time": "",
        }

