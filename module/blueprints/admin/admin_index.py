# -*- coding: utf-8 -*-
"""
@Time    : 2022/10/23 12:37
@Author  : ghwg
@File    : admin_index.py

"""
from flask import request, render_template, redirect, url_for, session, Blueprint, g, jsonify
from exts import limiter
from module.blueprints.admin import admin_login_check
from module.mod_post_requests import mod_post_data_info
from module.mysql.AdminClass import admin_class

admin_index_bp = Blueprint("admin_index", __name__, url_prefix="/admin")


# 后台主页
@admin_index_bp.route("/")
@limiter.exempt()
@admin_login_check
def admin_index():
    # 后台信息
    info = admin_class.get_admin_web_info()
    return render_template('admin/index.html', **info)


# 管理员登录
@admin_index_bp.route("/login", methods=["POST", "GET"])
@limiter.exempt()
def admin_login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    else:
        request_data = mod_post_data_info()  # 获取请求信息
        try:
            xuehao = request_data['username']
            password = request_data['password']
        except KeyError:
            return {"code": 500, "msg": "表单验证失败"}
        else:
            # 账号密码检测
            check_password_data = admin_class.check_admin_password(xuehao, password)

            # 账号密码校验 and 身份组检验
            if check_password_data:
                # 设置session
                session["admin_user"] = xuehao
                session["admin_password"] = password
                return {"code": 200, "msg": "登录成功"}  # 管理员后台
            else:
                return {"code": 400, "msg": "账号或密码错误"}


# 退出登录
@admin_index_bp.route("/logout", methods=["GET"])
@limiter.exempt()
def admin_logout():
    # 清除cookie
    session.clear()
    return redirect(url_for("admin_index.admin_login"))


# ajax获取网站信息api
@admin_index_bp.route("/ajax/info", methods=["POST", "GET"])
@limiter.exempt()
def admin_ajax_api():
    return jsonify(admin_class.get_admin_web_info())
