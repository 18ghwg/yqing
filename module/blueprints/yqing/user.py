# coding: utf-8
import asyncio
import time

from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify

from exts import limiter, db
from module.base import user_login_de_base
from module.emailcode import send_emailcode
from module.login_check import login_check
from module.mod_post_requests import mod_post_data_info
from module.mysql import UsersList, Emailcode, Emails, NADDUsers, Config
from module.mysql.CheckClass import check_class
from module.mysql.EmailClass import email_class
from module.mysql.UserClass import user_class
from module.mysql.WebClass import web_class
from module.mysql.modus import get_sql_info
from module.school.daka import check_user
from module.school.info import hq_webinfo
from module.send import sendwxbot, send_email
from tasks import user_daka

user_bp = Blueprint("user", __name__, url_prefix="/user")


# 检查是否为QQ数字邮箱
def check_nummail(_email: str):  # 检查是否是QQ数字邮箱
    if "@qq.com" in _email:  # 判断是否为QQ邮箱
        if len(_email.split("@")[0]) >= 6:  # 判断邮箱前缀长度
            try:
                int(_email.split("@")[0])
            except ValueError:
                return False
            else:
                return True
        else:
            return False
    else:
        return False


# 账号添加
@user_bp.route('/add', methods=['POST'])
@limiter.limit("20 per minute", override_defaults=False)  # 限流器
def add_user():
    request_data = mod_post_data_info()
    try:
        xuehao = request_data['addxuehao'].replace("+", "")
        mima = request_data['addmima']
        email = request_data['addemail']
        dk_time = request_data['dk_time'].replace("+", "")
    except KeyError:
        data_info = {"title": "参数有误", "count": "接收参数有误！",
                     "color": "983680", "span": "show"}
        return render_template("info.html", data=data_info)
    # 判断打卡时间
    if "：" in dk_time:
        dk_time = dk_time.replace("：", "")  # 中文符号替换
    else:
        try:  # 判断打卡在有效范围内
            dk_time_hour = int(dk_time.split(':')[0])  # 获取打卡小时
            if dk_time_hour < 7 or dk_time_hour >= 22:
                data_info = {"title": "时间有误", "count": "打卡时间有误\n学校服务器7:00-22:00开机！",
                             "color": "983680", "span": "show"}
                return render_template("info.html", data=data_info)
        except ValueError:
            data_info = {"title": "时间格式有误", "count": "打卡时间格式填写错误\n正确格式：00:00",
                         "color": "983680", "span": "show"}
            return render_template("info.html", data=data_info)
    checkdata = check_user(xuehao, mima)  # 密码检测
    if "超时" in str(checkdata):  # 登录超时
        info = {"xuehao": xuehao, "password": mima, "email": email, "dk_time": dk_time}
        if user_class.add_nadduser(info):  # 暂时添加到未提交用户表中
            # 设置session
            session['xuehao'] = xuehao
            session['password'] = mima
            return redirect(url_for('user.user_info'))  # 跳转到用户信息界面
        else:
            sendwxbot(f"教务处打卡网站链接超时！请管理员注意查看！\n网站：{web_class.get_web_config()['DKURL']}")
            data_info = {"title": "连接超时", "count": "教务系统服务器链接失败\n晚上会关闭服务器\n7:00开机——22:00关机！",
                         "color": "983680", "span": "show"}
            return render_template("info.html", data=data_info)  # 网站连接超时界面
    elif isinstance(checkdata, str):  # 登录出错
        data_info = {"title": "登陆失败", "count": f"{checkdata}",
                     "color": "e2d849", "span": "show"}
        return render_template("info.html", data=data_info)
    elif checkdata is False:
        data_info = {"title": "登陆失败", "count": f"不支持的账号类型",
                     "color": "e2d849", "span": "show"}
        return render_template("info.html", data=data_info)
    else:  # 密码正确: True
        if check_nummail(email):  # 检测邮箱格式是否正确
            if email_class.checkemail(email):  # 邮箱查重
                data_info = {"title": "邮箱重复", "count": "邮箱已被绑定！",
                             "color": "e2d849", "span": "show"}
                return render_template("info.html", data=data_info)
            else:
                if user_class.checkuser(xuehao):  # 学号查重
                    data_info = {"title": "重复提交", "count": "账号已存在\n请勿重复提交！",
                                 "color": "e2d849", "span": "show"}
                    return render_template("info.html", data=data_info)  # 账号重复界面
                else:
                    if not user_class.checkblack(xuehao):  # 黑名单查询
                        if send_emailcode(xuehao, mima, email, dk_time, 1200) is True:  # 发送邮箱验证
                            user_class.del_ndduser(xuehao)  # 删除未提交用户
                            # 设置session
                            session['xuehao'] = xuehao
                            session['password'] = mima
                            return redirect(url_for('user.user_info'))  # 跳转到用户信息界面
                        else:
                            data_info = {"title": "提交限制", "count": "当前账号发送邮件次数过多\n如果遇到问题请加群联系管理员！",
                                         "color": "e2d849", "span": "show"}
                            return render_template("info.html", data=data_info)
                    else:
                        data_info = {"title": "黑名单", "count": "nm黑名单账号!\n---------------\n交流群：685257643",
                                     "color": "CD0000FF", "span": "jiaqun"}
                        return render_template("info.html", data=data_info)  # 黑名单界面
        else:
            data_info = {"title": "邮箱有误", "count": "邮箱不正确\n请使用QQ[数字]邮箱！",
                         "color": "CD0000FF", "span": "show"}
            return render_template("info.html", data=data_info)


# 删除账号
@user_bp.route("/del", methods=["POST"])
@limiter.limit("1 per minute", override_defaults=False)  # 限流器
@login_check
def del_user():
    request_data = mod_post_data_info()
    xuehao = session['xuehao']
    beizhu = request_data['content']
    if user_class.deluser(xuehao, beizhu):  # 删除成功
        sendwxbot("`疫情打卡账号`<font color=\"warning\">删除了！</font>\n"
                  "**账号信息：**\n"
                  f">学号：<font color=\"info\">{xuehao}</font>\n"
                  f">备注：<font color=\"warning\">{beizhu}</font>")  # 发送账号删除提醒邮件
        session.clear()  # 清除session
        return {"code": 200, "msg": "账号删除成功！<br>江湖再见！"}
    else:  # 账号不存在
        return {"code": 400, "msg": "你的账号不存在<br>删个锤子！"}


# 登录
@user_bp.route('/login', methods=['GET', "POST"])
@limiter.exempt()
def user_login():
    if session.get('xuehao'):  # 如果已登录
        return redirect(url_for('user.user_info'))  # 跳转用户信息界面
    else:
        if request.method == 'GET':
            info = {"msg": "请先登录"}
            return render_template('user/login.html', **info)  # 跳转到登录界面
        else:  # POST
            login_time = int(time.time())  # 时间戳
            request_data = mod_post_data_info()
            xuehao = request_data['xuehao']
            password = user_login_de_base(request_data['password'])
            # 判断时间戳
            if str(login_time)[:-1] in password:
                # 处理密码
                password = password[:-len(str(login_time))]
            else:  # 前端请求的时间戳跟后端收到的时间戳相差太大
                return {"code": 400, "msg": "当前网络环境不良,不允许登录后台"}
            # 检查账号密码
            login_data = check_user(xuehao, password)
            if not login_data is False:
                if login_data is True or "超时" in login_data:
                    # session设置
                    session['xuehao'] = xuehao
                    session['password'] = password
                    # return redirect(url_for('user.user_info'))  # 跳转到用户后台
                    return {"code": 200, "msg": "用户登录成功"}
                else:  # 登录失败
                    # _data = {"msg": login_data}
                    # return render_template("user/login.html", **_data)
                    return {"code": 400, "msg": f"登录失败erro:{login_data}"}
            else:
                return {"code": 400, "msg": "登录失败erro:不支持的账号类型"}


# 退出登录
@user_bp.route('/logout', methods=['GET'])
def login_out():
    session.clear()  # 清除session信息
    return redirect('/')  # 跳转主页


# 用户后台
@user_bp.route('/info', methods=['GET'])
@limiter.exempt()
@login_check  # 检查session是否有效
def user_info():
    gonggao = get_sql_info(Config)['gg']  # 公告
    # 从session中获取数据
    xuehao = session['xuehao']  # 学号
    password = session['password']  # 密码
    # 获取用户其他数据
    userinfo = user_class.get_info(xuehao)  # 在数据库获取用户信息
    if userinfo:
        email = userinfo.get('email')  # 邮箱
        name = userinfo.get('name')  # 姓名
        clas = userinfo.get('clas')  # 班级
        gender = userinfo.get('gender')  # 性别
        qqh = userinfo.get('qqh')  # QQ号
        dk_info = userinfo.get('dk_info')  # 打卡信息状态：1：有历史打卡记录  0：无
        date = userinfo.get('date')  # 加入/发送/删除：日期
        dk_num = userinfo.get('dk_num')  # 打卡次数
        user_state = userinfo.get('user_state')  # 用户状态：0有效、1无效、2待验证、3已删除、4历史用户再添加、5未添加、6服务器没开机时提交的
        email_state = userinfo.get('email_state')  # 邮箱状态：0已验证、1待验证
        login_method = userinfo.get('login_method')  # 登录方式：add新用户、login已添加用户、logined历史用户、nadded未提交直接登录、nadded2服务器未开机提交的
        last_dk_time = userinfo.get('last_dk_time')  # 上次打卡日期
        room_num = userinfo.get('room_num')  # 宿舍号
        credit = userinfo.get('credit')  # 积分
        check_state = userinfo.get('check_state')  # 签到状态
        check_time = userinfo.get('check_time')  # 签到时间
        DKTimeUserNum = userinfo.get('DKTimeUserNum')  # 同打卡时间人数
        dk_time = userinfo.get('dk_time')  # 打卡时间
        QjmQuota = userinfo.get('QjmQuota')  # 额外请假数
        SendEmailUser = web_class.get_web_config()['SendEmailUser']  # 系统发送邮件的账号
        if user_state == 0 and DKTimeUserNum > 50:  # 修改到打卡人数较少的打卡时间
            user_class.mod_dk_time(xuehao, dk_time)
        info = {
            "xuehao": xuehao,
            "password": password,
            "email": {"email": email, "state": email_state},
            "name": name,
            "clas": clas,
            "gender": gender,
            "qqh": qqh,
            "dk_info": dk_info,
            "user_state": user_state,
            "dk_num": dk_num,
            "gonggao": gonggao,
            "date": date,
            "login_method": login_method,
            "last_dk_time": last_dk_time,
            "room_num": room_num,
            "friends_list": user_class.get_friends(clas),
            "credit": credit,
            "check_state": check_state,
            "check_time": check_time,
            "dk_time": dk_time,
            "DKTimeUserNum": DKTimeUserNum,
            "QjmQuota": QjmQuota,
            "SendEmailUser": SendEmailUser,
        }
    else:  # 没有提交过账号
        _user_info = hq_webinfo(xuehao, password)  # 在教务系统中获取信息
        if isinstance(_user_info, dict):  # dict-> 获取到用户信息
            name = _user_info.get('name')  # 姓名
            clas = _user_info.get('clas')  # 班级
            qqh = _user_info.get('qqh')  # QQ号
            dk_info = _user_info.get('dk_info')  # 打卡信息状态
            login_method = "nadded"  # 没有添加的用户
            info = {
                "name": name,
                "clas": clas,
                "qqh": qqh,
                "dk_info": dk_info,
                "gonggao": gonggao,
                "login_method": login_method,
                "user_state": 5,
                "email": {"email": '', "state": ''},
                "friends_list": user_class.get_friends(clas),
            }
        elif _user_info == "超时":  # 超时->添加到未提交用户界面
            _data = NADDUsers.query.filter_by(xuehao=xuehao).first()
            if _data:  # 是通过提交账号来的
                dk_time = _data.dk_time
                login_method = "nadded2"  # 没有添加的用户
                info = {
                    "name": '未知',
                    "clas": '未知',
                    "qqh": '1',
                    "dk_info": None,
                    "gonggao": gonggao,
                    "login_method": login_method,
                    "user_state": 6,
                    "email": {"email": '', "state": ''},
                    "dk_time": dk_time,
                }
            else:  # 没提交账号-> 用户直接登录来的获取不到信息
                data_info = {"title": "连接超时", "count": "教务系统服务器链接失败\n晚上会关闭服务器\n7:00开机——22:00关机！",
                             "color": "983680", "span": ""}
                # session.clear()  # 清理session
                return render_template("info.html", data=data_info)  # 网站连接超时界面
        else:  # False-> 账号或密码错误
            data_info = {"title": "登录失败", "count": "登录学校网站时->登录失败！\n可能账号或密码错误\n已自动退出登录！",
                         "color": "983680", "span": "show"}
            session.clear()  # 清理session
            return render_template("info.html", data=data_info)  # 网站连接超时界面

    return render_template("user/index.html", **info)


# 更新用户信息
@user_bp.route('/info/put', methods=['GET', 'POST'])
@limiter.limit("10 per minute", override_defaults=False)
@login_check
def put_info():
    xuehao = session['xuehao']  # 学号
    password = session['password']  # 密码
    if xuehao is None:  # 没登录
        return redirect(url_for('user.user_login'))
    if request.method == 'GET':
        # 获取用户其他数据
        userinfo = user_class.get_info(xuehao)  # 在数据库获取用户信息
        if userinfo:
            email = userinfo.get('email')  # 邮箱
            name = userinfo.get('name')  # 姓名
            clas = userinfo.get('clas')  # 班级
            gender = userinfo.get('gender')  # 性别
            qqh = userinfo.get('qqh')  # QQ号
            dk_time = userinfo.get('dk_time')  # 打卡时间
            dk_num = userinfo.get('dk_num')  # 打卡次数
            user_state = userinfo.get('user_state')  # 用户状态：0有效、1无效、2待验证、3已删除 4已删除重新添加
            email_state = userinfo.get('email_state')  # 邮箱状态：0已验证、1待验证
            room_num = userinfo.get('room_num')  # 宿舍号
            if room_num is None:  # 空值处理
                room_num = ''
            info = {
                "xuehao": xuehao,
                "password": password,
                "email": {"email": email, "state": email_state},
                "name": name,
                "clas": clas,
                "gender": gender,
                "qqh": qqh,
                "user_state": user_state,
                "dk_num": dk_num,
                "dk_time": dk_time,
                "room_num": room_num,
            }
        else:  # 用户不存在
            _data = NADDUsers.query.filter_by(xuehao=xuehao).first()
            info = {
                "xuehao": xuehao,
                "password": password,
                "user_state": 6,
                "email": {"email": None, "state": None},
            }
            if _data:  # 在服务器关闭时添加的用户
                info['user_state'] = 6
            else:  # 学校服务器开机
                info['user_state'] = 5
        return render_template('user/put.html', **info)  # 信息修改界面

    else:  # POST更新信息的方法
        kv = mod_post_data_info()  # 获取请求信息
        try:
            _email = kv['email']
            _password = kv['password']
            _qqh = int(kv['qqh'])
            _user_state = int(kv['user_state'])
            _dk_time = kv['dk_time']  # 打卡时间
            _room_num = kv['room_num']  # 宿舍号
        except (KeyError, ValueError):
            return {"code": 400, "msg": "接收参数有误！"}
        else:
            if int(_dk_time.split(':')[0]) < 7 or int(_dk_time.split(':')[0]) >= 22:
                return {"code": 400, "msg": "打卡时时间不正确！学校服务器开机时间：7至22点"}
            if _email == '' or _password == '' or _qqh == '' or _user_state == '' or _dk_time == '':
                return {"code": 400, "msg": "更新失败：参数为空！"}
            if check_nummail(_email) is False:
                return {"code": 400, "msg": "请修改为QQ数字邮箱！"}
            _check_data = check_user(xuehao, _password)  # 密码检查
            _check_email = email_class.check_email2(_email, xuehao)  # 邮箱重复检查
            if _password == password:  # 如果密码没改变，默认密码是有效的
                _check_data = True
            if _check_data is True:  # 密码校验成功
                if _check_email is False or isinstance(_check_email, str):  # 邮箱校验成功
                    if _user_state == 0 or _user_state == 1:  # 有效用户和禁用用户
                        user_data = UsersList.query.filter_by(xuehao=xuehao).first()  # 根据session中的学号来识别用户
                        user_data.password = _password
                        user_data.qqh = _qqh
                        user_data.dk_time = _dk_time
                        user_data.state = 0
                        if _room_num != '':  # 没有修改宿舍号
                            user_data.room_num = _room_num
                        email_data = Emails.query.filter_by(id=user_data.email_id).first()
                        email_data.email = _email
                    elif _user_state == 2 or _user_state == 4:  # 待验证用户
                        for i in range(0, 3):
                            emailcode_data = Emailcode.query.filter_by(xuehao=xuehao).first()
                            if emailcode_data:
                                emailcode_data.password = _password
                                emailcode_data.qqh = _qqh
                                emailcode_data.email = _email
                                emailcode_data.dk_time = _dk_time
                                if _room_num != '':  # 没有修改宿舍号
                                    emailcode_data.room_num = _room_num
                                break  # 退出整个循环
                            else:
                                continue  # 退出当前循环
                    elif _user_state == 3:  # 已删除用户
                        return {"code": 400, "msg": "已删除用户，不支持更改信息"}
                    elif _user_state == 6:  # 服务器关闭
                        return {"code": 400, "msg": "你都没提交账号，更新个锤子！"}
                    db.session.commit()  # 提交数据
                    session['password'] = _password  # 更新session密码
                    if isinstance(_check_email, str):  # 待验证
                        if send_emailcode(xuehao, _password, _email, _dk_time, 1200) is True:  # 发送验证邮件
                            return {"code": 200, "msg": "邮箱修改成功<br>还需要重新验证你的邮箱！"}
                        else:  # 超过最大发送限制
                            return {"code": 400, "msg": "邮件发送超过最大限制<br>联系管理员处理！"}
                    else:
                        return {"code": 200, "msg": "信息修改成功"}
                else:
                    return {"code": 400, "msg": "你所填写的邮箱已被占用！"}
            elif "超时" in _check_data:
                return {"code": 400, "msg": "密码校验失败：学校服务器关机！白天再来！"}
            else:  # 登陆失败
                return {"code": 400, "msg": f"{_check_data}"}


# 获取用户信息api
@user_bp.route("info/ajax", methods=["POST", "GET"])
@limiter.exempt()  # 限流器
def user_info_ajax():
    info = {"user": {}, "qjm": {}}  # 用户信息
    # 获取信息
    xuehao = session.get('xuehao')
    if xuehao:
        # 获取用户主要信息
        _info = user_class.get_info(xuehao)
        # 获取请假码配置
        if _info:  # 搜到用户了
            info["user"]["state"] = _info["user_state"]  # 用户状态
            if info["user"]["state"] == 0:  # 账号有效
                info["user"]["credit"] = _info["credit"]  # 用户积分
                info["user"]["QjmQuota"] = _info["QjmQuota"]  # 请假名额
                info["user"]["check_state"] = _info["check_state"]  # 签到状态
                info["user"]["DKTimeUserNum"] = _info["DKTimeUserNum"]  # 同时间打卡人数
                info["user"]["dk_time"] = str(_info["dk_time"])  # 同时间打卡人数
                info["user"]["dk_num"] = _info["dk_num"]  # 打卡次数
            return jsonify(info)
        else:  # 用户不在表中
            # session.clear()  # 清除session
            return jsonify({"code": 400, "msg": "还没提交账号"})
    else:
        session.clear()  # 清除登录信息
        return jsonify({"code": 400, "msg": "登录失效"})


# 打卡
@user_bp.route("/dk", methods=["POST"])
@limiter.limit("3 per minute", override_defaults=False)  # 限流器
@login_check
def user_dk():
    xuehao = session.get('xuehao')
    if xuehao:
        return user_daka(xuehao)
    else:  # 没登录
        return redirect(url_for('user.user_login'))


# 发送反馈
@user_bp.route("/fk", methods=["POST"])
@limiter.exempt()
@login_check
def send_fk():
    kv = mod_post_data_info()
    # 接收数据
    subject = kv['subject']  # 主题
    content = kv['content']  # 反馈内容
    if subject == '' or content == '':
        return {"code": 400, "msg": "参数有误！"}
    # 数据处理
    xuehao = session.get('xuehao')
    userinfo = user_class.get_info(xuehao)  # 在数据库获取用户信息
    if xuehao:
        if userinfo:
            user_email = userinfo['email']  # 用户邮箱
            admin_email = web_class.get_web_config()["AdminEmail"]  # 管理员邮箱
            asyncio.run(send_email(admin_email, content + f'<br><hr>用户信息：<br>邮箱：{user_email}  学号：{xuehao}',
                                   f'疫情打卡反馈：{subject}'))
            return {"code": 200, "msg": "反馈已提交！"}
        else:
            return {"code": 400, "msg": "提交失败，获取用户信息失败！"}
    else:
        return redirect(url_for('user.user_login'))


# 用户签到
@user_bp.route("/check", methods=["POST"])
@limiter.exempt()
@login_check
def UserCheck():
    xuehao = session.get("xuehao")  # 学号
    check_info = check_class.user_check(xuehao)  # 获取签到信息
    return check_info


