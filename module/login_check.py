# 检测是否登陆
from flask import g, redirect, url_for
from functools import wraps


def login_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'xuehao'):
            return func(*args, **kwargs)
        else:

            return redirect(url_for('user.user_login'))

    return wrapper
