# 验证邮箱接口
import json
from flask import Blueprint, request, render_template, session
from module.emailcode import verify_emailcode, send_emailcode
from module.login_check import login_check
from module.mysql.EmailClass import email_class
from module.mysql.UserClass import user_class
from exts import limiter
from module.mysql.WebClass import web_class

emailcode_bp = Blueprint("emailcode", __name__, url_prefix="/emailcode")


# 验证邮箱
@emailcode_bp.route('/', methods=['GET'])
@limiter.limit("5 per minute", override_defaults=False, error_message="别闹！：频繁请求！过会再来验证！")  # 限流器
def emailcode():
    # 获取get参数
    email = request.args.get('email', type=str)
    code = request.args.get('code', type=int)
    # print(email, code)
    return render_template("info.html", data=verify_emailcode(email, code))


# 删除验证码
@emailcode_bp.route('/del', methods=['GET'])
@limiter.limit("3/minute", override_defaults=False, error_message="别闹！：频繁请求")  # 限流器
def del_emailcode():
    email = request.args.get('email')  # 邮箱
    _deldata = email_class.delemailcode(email)
    if _deldata:  # 删除成功
        info = {"title": "删除成功", "count": "验证信息删除成功！", "color": "20a162", "span": "show"}
    else:
        info = {"title": "删除失败", "count": "没有找到你的信息\n你可以加群处理！", "color": "d2b116", "span": "jiaqun"}
    return render_template('info.html', data=info)


# 发送邮箱验证码
@emailcode_bp.route('/send', methods=['POST'])
@limiter.limit("5/minute", override_defaults=False, error_message="别闹！：频繁请求")  # 限流器
@login_check
def send_mailcode():
    # 从session中获取数据
    xuehao = session['xuehao']  # 学号
    password = session['password']  # 密码
    # 获取用户其他数据
    userinfo = user_class.get_info(xuehao)  # 在数据库获取用户信息
    dk_time = userinfo.get('dk_time')  # 打卡时间
    if isinstance(userinfo, dict):
        email = userinfo.get('email')  # 邮箱
        send_data = send_emailcode(xuehao, password, email, dk_time, 1200)
        if send_data is True:
            return {"code": 200, "msg": "已发送验证邮件,请前往邮箱验证！"}
        elif isinstance(send_data, str):
            return {"code": 400, "msg": "当前账号发送次数过多,联系管理员处理！"}
    else:
        return {"code": 400, "msg": "验证码发送失败！没有找到验证信息！"}
