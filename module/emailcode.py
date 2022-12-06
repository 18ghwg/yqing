# 邮箱验证码
import asyncio
import random
from datetime import datetime

from flask import url_for

from config import logger
from exts import db
from module.mysql import Emailcode
from module.mysql.CreditClass import credit_class
from module.mysql.EmailClass import email_class
from module.mysql.UserClass import user_class
from module.mysql.WebClass import web_class
from module.school.info import hq_webinfo
from module.send import send_email, sendwxbot


# 处理QQ号号
def mod_qqh(_email):
    if '@qq.com' in _email:
        _qqh = _email.split('@')[0]
        try:
            _qqh = int(_qqh)
        except ValueError:
            _qqh = 1
        else:
            return _qqh
    else:
        return None


# 发送邮件验证码
def send_emailcode(xuehao: str, password: str, email: str, dktime: datetime.time, verify_time: int):
    """
    :param xuehao: 学号
    :param password: 密码
    :param email: 邮箱
    :param dktime: 打卡时间
    :param verify_time: 验证超时时间
    :return: False：登录超时或账号密码错误  True：发送成功  str：次数限制
    """
    # 在数据库中搜索信息
    user_info = user_class.get_info(xuehao)
    if isinstance(user_info, dict):  # 获取到信息
        name = user_info.get('name')  # 姓名
        clas = user_info.get('clas')  # 班级
        gender = user_info.get('gender')  # 性别
        qqh = user_info.get('qqh') if user_info.get("qqh") else mod_qqh(email)  # QQ
        dk_info = user_info.get('dk_info')  # 打卡信息状态
        room_num = user_info.get('room_num')  # 宿舍号
        logger.info("在数据库获取到信息了")
        # print("在数据库获取到信息了")
    else:
        # 获取在校信息
        info_data = hq_webinfo(xuehao, password)
        if isinstance(info_data, dict):  # 获取信息成功
            name = info_data.get('name')  # 姓名
            clas = info_data.get('clas')  # 班级
            gender = info_data.get('gender')  # 性别
            qqh = info_data.get('qqh') if info_data.get("qqh") else mod_qqh(email)  # QQ
            dk_info = info_data.get('dk_info')  # 打卡信息状态
            room_num = info_data.get('room_num')  # 宿舍号
            # print("获取到在线信息")
        else:  # 登录超时或者账号密码错误
            # print("登录超时")
            return False
    # 生成验证码
    mail_code = random.randint(000000, 999999)
    # 存储验证信息
    emailcode_info = Emailcode.query.filter_by(xuehao=xuehao).all()  # 查询验证信息
    if len(emailcode_info) == 1:  # 如果已存在一条信息 -> 更新
        emailcode_info[0].email = email
        emailcode_info[0].email_code = mail_code
        emailcode_info[0].xuehao = xuehao
        emailcode_info[0].password = password
        emailcode_info[0].name = name
        emailcode_info[0].clas = clas
        emailcode_info[0].gender = gender
        emailcode_info[0].qqh = qqh
        emailcode_info[0].room_num = room_num
        emailcode_info[0].dk_info = dk_info
        emailcode_info[0].dk_time = dktime
        emailcode_info[0].time = datetime.now()
        emailcode_info[0].send_num += 1  # 验证码发送次数加一
        send_num = emailcode_info[0].send_num  # 获取发送邮件数量
        emailcode_info[0].verify_time = verify_time
    elif len(emailcode_info) > 1:  # 有多条验证信息
        send_num = 1
        Emailcode.query.filter_by(xuehao=xuehao).delete()  # 删除所有验证信息
        emailcode_addinfo = Emailcode(email=email, email_code=mail_code, xuehao=xuehao, password=password,
                                      name=name, clas=clas, gender=gender, qqh=qqh,
                                      dk_info=dk_info, dk_time=dktime, send_num=send_num,
                                      verify_time=verify_time, room_num=room_num)
        db.session.add(emailcode_addinfo)
    else:  # 新增
        send_num = 1
        emailcode_addinfo = Emailcode(email=email, email_code=mail_code, xuehao=xuehao, password=password,
                                      name=name, clas=clas, gender=gender, qqh=qqh,
                                      dk_info=dk_info, dk_time=dktime, send_num=send_num,
                                      verify_time=verify_time, room_num=room_num)
        db.session.add(emailcode_addinfo)

    logger.info(f"第{send_num}次尝试发送邮件！")

    if send_num <= email_class.get_sendemail_maxnum():  # 限制发送邮件次数
        db.session.commit()  # 提交
        # 发送邮件
        can = f"{web_class.get_web_config()['WebUrl']}/emailcode?code={mail_code}&email={email}"
        nr = f'这是一封验证邮件，点击链接以验证你的邮箱！<br>点此已验证：<a href="{can}">{can}</a>'
        asyncio.run(send_email(email, nr, '验证邮件'))
        return True
    else:
        logger.info("当前学号超过邮箱最大发送次数！联系管理员处理吧！")
        return "当前学号超过邮箱最大发送次数！联系管理员处理吧！"


# 验证邮箱
def verify_emailcode(email: str, code: int):
    emailcode_info = Emailcode.query.filter_by(email=email).first()  # 读取数据库信息
    if emailcode_info:  # 读取到信息
        _email = emailcode_info.email  # 邮箱
        xuehao = emailcode_info.xuehao  # 学号
        password = emailcode_info.password  # 密码
        email_code = emailcode_info.email_code  # 验证码
        name = emailcode_info.name  # QQ
        clas = emailcode_info.clas  # 班级
        gender = emailcode_info.gender  # 性别
        qqh = emailcode_info.qqh  # QQ
        room_num = emailcode_info.room_num  # 宿舍号
        dk_info = emailcode_info.dk_info  # 打卡信息状态
        dk_time = emailcode_info.dk_time  # 打卡时间
        verify_time = emailcode_info.verify_time  # 验证超时时间

        info = {"xuehao": xuehao, "password": password, "email": _email, "name": name,
                "clas": clas, "gender": gender, "qqh": qqh, "dk_info": dk_info,
                "dk_time": dk_time, "room_num": room_num,
                }
        # 防止用户反复注册获得初始积分
        # _del_data = DelUsersed.query.filter_by(xuehao=xuehao).first()
        # if _del_data:  # 删除过得用户回来了
        #     info["last_dk_time"] = _del_data.last_dk_time  # 上次打卡日期
        #     info["credit"] = 0
        # else:  # 新用户
        # 获取新加入积分配置
        credit = credit_class.get_credit_config()["JoinCredit"]
        info["credit"] = credit
        pass
        if email == _email and code == email_code:  # 数据检查
            if (datetime.now() - datetime.strptime(str(emailcode_info.time),
                                                   "%Y-%m-%d %H:%M:%S")).seconds < verify_time:  # 超时验证
                user_class.adduser(info)  # 添加数据
                email_class.delemailcode(email)  # 删除验证信息
                asyncio.run(send_email(email, f"你的账号{xuehao}已成功添加！<br>打卡将于明天早上{dk_time}开始陆续打卡！", '账号添加提醒'))
                sendwxbot("收到新的`疫情打卡账号`"
                          "\n>**账号信息：**"
                          f"\n>学号：<font color=\"info\">{xuehao}</font>"
                          f"\n>邮箱：<font color=\"warning\">{email}</font>"
                          f"\n>姓名：<font color=\"info\">{name}</font>"
                          f"\n>班级：<font color=\"warning\">{clas}</font>"
                          f"\n>性别：<font color=\"info\">{gender}</font>"
                          f"\n>打卡时间：<font color=\"warning\">{dk_time}</font>")
                data_info = {"title": "验证成功", "count": "邮箱验证成功\n----------------\n账号已提交！", "color": "20a162",
                             "span": "jiaqun"}
                return data_info  # 成功页面
            else:
                data_info = {"title": "验证超时", "count": "邮箱验证超时\n重新提交验证即可！", "color": "F14F4FFF", "span": ""}
                return data_info
        else:
            data_info = {"title": "参数有误", "count": "邮箱验证失败\n参数不正确！", "color": "F14F4FFF", "span": "jiaqun"}
            return data_info
    else:
        data_info = {"title": "验证出错", "count": "邮箱验证出错\n你有没有提交账号？",
                     "color": "F14F4FFF", "span": "jump", "url": f"{url_for('user.user_info')}"}
        return data_info
