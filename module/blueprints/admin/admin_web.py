# -*- coding: utf-8 -*-
"""
@Time    : 2022/10/25 13:10
@Author  : ghwg
@File    : admin_web.py

"""
from datetime import datetime

from flask import request, render_template, Blueprint
from exts import limiter
from module.blueprints.admin import admin_login_check
from module.mod_post_requests import mod_post_data_info
from module.mysql import Config
from module.mysql.modus import get_sql_info, put_sql_info

admin_web_bp = Blueprint("admin_web", __name__, url_prefix="/admin")


# Web信息设置
@admin_web_bp.route("/webset", methods=["POST", "GET"])
@limiter.exempt()
@admin_login_check
def web_info():
    if request.method == "GET":
        info_list = get_sql_info(Config)  # 获取网站配置
        return render_template('admin/info/web/web-info.html', **info_list)
    else:
        kv = mod_post_data_info()  # 获取请求信息
        try:
            webname = kv['webname']  # 网站名称
            weburl = kv['weburl']  # 网站链接
            dkurl = kv['weburl_student']  # 学校打卡网站链接
            web_gg = kv['gg']  # 网站公告
            qq_group_url = kv['qq_group_url']  # QQ群url
        except KeyError:
            return {"code": 500, "msg": "参数有误"}
        else:
            # 更新配置
            sql_data = {
                "WebName": webname,
                "WebUrl": weburl,
                "DKURL": dkurl,
                "gg": web_gg,
                "QQGroupUrl": qq_group_url,
            }
            gg_data = Config.query.get(1)
            if gg_data.gg != web_gg:  # 如果修改了公告内容
                sql_data["putdate"] = datetime.now()  # 更新时间
            else:
                pass
            put_sql_info(Config, sql_data)
            return {"code": 200, "msg": "网站配置已更新"}


# 企业微信设置
@admin_web_bp.route("/qyinfo", methods=["POST", "GET"])
@limiter.exempt()
@admin_login_check
def qy_info():
    if request.method == "GET":
        info_list = get_sql_info(Config)  # 获取网站配置
        return render_template('admin/info/web/qy-info.html', **info_list)
    else:
        kv = mod_post_data_info()  # 获取请求信息
        try:
            CorpID = kv['CorpID']  # 企业id
            AccessToken = kv['AccessToken']  # 企业密钥
            AgentID = kv['AgentID']  # 应用id
            CorpSecret = kv['CorpSecret']  # 应用密钥
        except KeyError:
            return {"code": 500, "msg": "参数有误"}
        else:
            # 更新配置
            sql_data = {
                "CorpID": CorpID,
                "AccessToken": AccessToken,
                "AgentID": AgentID,
                "CorpSecret": CorpSecret
            }
            put_sql_info(Config, sql_data)
            return {"code": 200, "msg": "企业微信配置已更新"}


# 邮件配置
@admin_web_bp.route("/emailinfo", methods=["POST", "GET"])
@limiter.exempt()
@admin_login_check
def email_info():
    if request.method == "GET":
        info_list = get_sql_info(Config)  # 获取网站配置
        return render_template('admin/info/web/email-info.html', **info_list)
    else:
        kv = mod_post_data_info()  # 获取请求信息
        try:
            AdminEmail = kv['AdminEmail']  # 管理员邮箱
            SendEmailUser = kv['SendEmailUser']  # 邮箱账号
            SendEmailPassword = kv['SendEmailPassword']  # 邮箱密码
            SendEmailStmp = kv['SendEmailStmp']  # 邮箱服务器地址
            SendEmailPort = kv['SendEmailPort']  # 邮箱服务器端口
            SendEmailMaxNum = kv['SendEmailMaxNum']  # 验证码最大发送次数
            SendFailMaxNum = kv['SendFailMaxNum']  # 邮件拒收最大数量
            EmailGG = kv['emailcontent_temp']  # 邮件公告
        except KeyError:
            return {"code": 500, "msg": "参数有误"}
        else:
            # 更新配置
            sql_data = {
                "AdminEmail": AdminEmail,
                "SendEmailUser": SendEmailUser,
                "SendEmailPassword": SendEmailPassword,
                "SendEmailMaxNum": SendEmailMaxNum,
                "SendEmailStmp": SendEmailStmp,
                "SendEmailPort": SendEmailPort,
                "SendFailMaxNum": SendFailMaxNum,
                "EmailGG": EmailGG
            }
            put_sql_info(Config, sql_data)
            return {"code": 200, "msg": "邮件配置已更新"}


# 机器人配置
@admin_web_bp.route("/bot/info", methods=["POST", "GET"])
@limiter.exempt()
@admin_login_check
def bot_info():
    if request.method == "GET":
        info_list = get_sql_info(Config)  # 获取网站配置
        return render_template('admin/info/web/bot-info.html', **info_list)
    else:
        kv = mod_post_data_info()  # 获取请求信息
        try:
            managerids = kv['managerids']  # 管理员id
            groups = kv['groups']  # 机器人响应QQ群
        except KeyError:
            return {"code": 500, "msg": "参数有误"}
        else:
            # 更新配置
            sql_data = {
                "Managers": managerids,
                "Groups": groups,
            }
            put_sql_info(Config, sql_data)
            return {"code": 200, "msg": "机器人配置已更新"}


# 机器人配置json接口
@admin_web_bp.route("/bot/config", methods=["GET"])
@limiter.exempt()
def bot_config():
    # 获取网站配置
    bot_config_data = get_sql_info(Config)
    if bot_config_data:
        # 处理管理员列表
        managers = bot_config_data["Managers"]  # 管理员id/QQ
        manager_list = [int(ID) for ID in str(managers).split(",")]  # 管理员列表

        # 处理QQ群列表
        groups = bot_config_data["Groups"]  # 群组id
        group_list = [int(ID) for ID in groups.split(",")]  # 群组列表
        return {"code": 200, "group": group_list, "manager": manager_list}
    else:  # 获取信息为空
        return {"code": 400, "group": "", "manager": ""}


