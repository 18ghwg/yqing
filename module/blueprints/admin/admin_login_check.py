# -*- coding: utf-8 -*-
"""
@Time    : 2022/10/25 13:14
@Author  : ghwg
@File    : admin_login_check.py

"""
from functools import wraps
from flask import session, redirect, url_for, g
from module.mysql.AdminClass import admin_class


# 检测管理员登录状态
def admin_login_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        admin = g.get('admin_user')  # 管理员账号
        password = g.get('admin_password')  # 管理员密码
        # 登录状态检测and账号密码检查
        check_data = admin_class.check_admin_password(admin, password)
        if hasattr(g, 'admin_user') and check_data:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('admin_index.admin_login'))

    return wrapper
