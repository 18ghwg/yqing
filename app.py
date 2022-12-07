# coding=utf-8

from flask import render_template, request, session, g
from flask_apscheduler import APScheduler
from flask_migrate import Migrate

import config
from config import logger
from exts import db, app, limiter
from module.blueprints import emailcode_bp
from module.blueprints.admin import admin_index_bp, admin_web_bp, admin_credit_bp, admin_user_bp
from module.blueprints.yqing import user_bp
from module.mysql import Config
from module.mysql.UserClass import user_class
from module.mysql.WebClass import web_class
from module.mysql.modus import get_sql_info
from module.school.daka import check_user
from module.send import sendwxbot
from tasks import Config as TaskConfig

scheduler = APScheduler()  # 实例化
app.config.from_object(config)
app.config.from_object(TaskConfig())  # 载入定时任务配置
db.init_app(app)  # 初始化数据库
migrate = Migrate(app, db)  # 实例化蓝图

app.register_blueprint(user_bp)  # 操作user接口
app.register_blueprint(emailcode_bp)  # 邮箱验证码接口
# admin后台接口
app.register_blueprint(admin_index_bp)  # 后台主页
app.register_blueprint(admin_web_bp)  # 网站设置
app.register_blueprint(admin_credit_bp)  # 积分设置
app.register_blueprint(admin_user_bp)  # 用户设置


@app.route('/')
@limiter.exempt()  # 禁用全局限流器
def index():
    people_num = user_class.get_user_num()  # 使用人数
    web_data = get_sql_info(Config)  # 获取网站配置
    info = {
        "num": people_num,
        "gonggao": web_data['gg'],
        "date": web_data['putdate'],
        "WebName": web_data['WebName'],
    }
    return render_template("index.html", **info)


@app.errorhandler(500)
@limiter.exempt()
def erro_500(e):
    _data = request.get_data().decode('utf-8')  # 收到的请求数据
    _method = request.method  # 请求方法：GET/POST
    _url = request.url  # 发送请求的url
    _xuehao = session.get("xuehao")  # 触发错误的用户
    nr = f"疫情打卡网站出现500错误！\n{web_class.get_web_config()['WebUrl']}\n错误：\n请求方法：{_method}\n请求url:{_url}\n收到数据：{_data}\n用户：{_xuehao}"
    sendwxbot(nr)
    return render_template('500.html'), 500


@app.errorhandler(404)
@limiter.exempt()
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(405)
@limiter.exempt()
def erro_xianliu(e):
    _data = request.get_data().decode('utf-8')  # 收到的请求数据
    _method = request.method  # 请求方法：GET/POST
    _url = request.url  # 发送请求的url
    if '/user/' in _url:
        return "异常请求"
    elif '/emailcode' in _url:
        return "异常请求"
    elif '/black' in _url:
        return "异常请求"
    else:
        sendwxbot(f"疫情打卡网站：\n收到异常请求：\n方法：{_method}\nURL：{_url}\n参数：\n{_data}")
        return render_template('405.html'), 405


# 频繁请求
@app.errorhandler(429)
@limiter.exempt()
def page_not_found(e):
    return render_template('429.html'), 429


# 服务器请求前做的工作
@app.before_request
def before_request():
    session.permanent = True  # 开启session有效期设置
    # 用户
    xuehao = session.get('xuehao')
    password = session.get('password')
    if xuehao and password:  # 如果获取到用户信息了
        # 设置用户信息
        setattr(g, 'xuehao', xuehao)
        setattr(g, 'password', password)
    # 管理员
    admin_user = session.get('admin_user')  # 管理员账号
    admin_password = session.get('admin_password')  # 管理员密码
    if admin_user and admin_password:
        # 设置管理员信息
        setattr(g, 'admin_user', admin_user)
        setattr(g, 'admin_password', admin_password)
    # 每次请求接口前打印接口信息
    _data = request.get_data()
    if str(_data) == "b\'\'":  # 请求信息为空
        pass
    else:
        logger.info(f"【收到请求】获取到请求信息：{_data}")


# 上下文处理器
# 给模板传值
@app.context_processor
def context_processor():
    web_config = web_class.get_web_config()  # 网站配置
    if hasattr(g, 'xuehao'):  # 如果已经登录
        info = {"xuehao": g.xuehao}
        info.update(web_config)  # 加入网站配置
        return info
    else:
        return {}


if __name__ == '__main__':
    limiter.init_app(app)  # 初始化限流器
    scheduler.init_app(app)  # 初始化定时任务
    scheduler.start()  # 启动定时任务
    app.run(host="127.0.0.1", port=5101, debug=True)
