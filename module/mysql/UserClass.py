# 数据库操作
import random
from datetime import datetime, timedelta, time
from typing import Union

from sqlalchemy import func

from config import logger, credit_method
from exts import db, app
from module import sendwxbot
from module.mysql import UsersList, Black, Emails, Emailcode, NADDUsers, NotStudentUser
from module.mysql.CheckClass import check_class
# 用户类
from module.mysql.CreditClass import credit_class
from module.mysql.modus import get_sql_list, search_sql_info


class UserClass:
    # 检查用户是否存在
    @classmethod
    def checkuser(cls, xuehao: str) -> bool:
        """
        :param xuehao: 学号
        :return: True:存在  False:不存在
        """
        check_data = UsersList.query.filter_by(xuehao=xuehao).first()

        if check_data:
            if UsersList.query.filter_by(xuehao=xuehao).first():  # 第二次查重
                state = check_data.state  # 用户状态
                if state == 0:  # 账号有效
                    return True
                else:  # 账号无效
                    return False
            else:
                return False
        else:  # 用户不存在
            return False

    # 比对账号密码
    @classmethod
    def check_user_password(cls, xuehao: str, password: str):
        _data = UsersList.query.filter_by(xuehao=xuehao, password=password).first()
        if _data:
            return True
        else:
            return False

    # 添加用户
    @classmethod
    def adduser(cls, info: dict) -> bool:
        """
        :param info: 提交信息
        :return: True: 添加成功  False:用户已存在
        """
        xuehao = info.get('xuehao')
        password = info.get('password')
        email = info.get('email')
        name = info.get('name')
        clas = info.get('clas')
        gender = info.get('gender')
        qqh = info.get('qqh')
        dk_info = info.get('dk_info')
        dk_time = info.get('dk_time')
        last_dk_time = info.get('last_dk_time')
        room_num = info.get('room_num')  # 宿舍号
        credit = info.get('credit')  # 积分
        # 获取打卡次数
        # dk_num_data = DelUsersed.query.filter_by(xuehao=xuehao).first()  # 在历史用户表中搜索数据
        user_state_data = UsersList.query.filter_by(xuehao=xuehao).first()  # 搜索用户
        # if dk_num_data:  # 用户存在历史用户列表中
        #     dk_num = dk_num_data.dk_num  # 获取用户之前的打卡次数
        # else:  # 新用户
        dk_num = 0
        if not user_state_data:  # 用户不存在数据库
            if int(xuehao) == 2003460310:  # 识别到管理员
                logger.info("检测到admin，自动前移")
                user_info = UsersList(id=1, xuehao=xuehao, password=password, room_num=room_num,
                                      name=name, gender=gender, clas=clas, qqh=qqh, credit=credit,
                                      dk_time=dk_time, dk_info=dk_info, dk_num=dk_num, last_dk_time=last_dk_time)
                email_info = Emails(email=email)  # 创建邮箱
                user_info.email = email_info  # 在users表中生成对应的email_id
            else:  # 普通用户
                user_info = UsersList(xuehao=xuehao, password=password, room_num=room_num,
                                      name=name, gender=gender, clas=clas, qqh=qqh, credit=credit,
                                      dk_time=dk_time, dk_info=dk_info, dk_num=dk_num, last_dk_time=last_dk_time)
                email_info = Emails(email=email)  # 创建邮箱
                user_info.email = email_info  # 在users表中生成对应的email_id
            db.session.add(user_info)  # 创建任务
            db.session.commit()  # 提交
            return True
        else:  # 用户在数据库中
            _email_data = Emails.query.filter_by(id=user_state_data.email_id).first()  # 搜索邮箱
            state = user_state_data.state  # 获取状态
            if state == 1 or state == 2:  # 无效用户: 去更新变量
                user_state_data.password = password
                user_state_data.state = 0
                user_state_data.qqh = qqh
                user_state_data.dk_info = dk_info
                user_state_data.dk_time = dk_time
                user_state_data.room_num = room_num
                _email_data.email = email  # 更新邮箱
                db.session.commit()  # 提交
                return True
            else:  # 有效用户, 重复添加
                logger.info("添加用户：用户重复不做处理！")
                return False

    # 删除用户
    def deluser(self, xuehao: str, beizhu: str) -> bool:
        """
        :param xuehao: 学号
        :param beizhu: 备注
        :return: True:删除成功 Flase:账号不存在
        """
        if self.checkuser(xuehao):  # 账号存在
            searchdata = UsersList.query.filter_by(xuehao=xuehao).first()  # 获取用户信息
            UsersList.query.filter_by(xuehao=xuehao).delete()  # 删除用户  先删除子类
            Emails.query.filter_by(iD=searchdata.email_id).delete()  # 删除用户邮箱  后删除父类
            QJM.query.filter_by(xuehao=xuehao).delete()  # 删除请假信息
            db.session.commit()  # 提交
            return True
        else:
            return False

    # 添加到未提交表中
    @classmethod
    def add_nadduser(cls, info: dict):
        """
        :param info: 用户信息
        :return: False：用户存在于表中 True：添加成功
        """
        xuehao = info.get('xuehao')
        password = info.get('password')
        email = info.get('email')
        dk_time = info.get('dk_time')

        _data = NADDUsers.query.filter_by(xuehao=xuehao).first()
        if cls.search_user_all(xuehao) is False:  # 用户不存在用户表中
            if _data:  # 已存在
                _data.password = password
                _data.email = email
                _data.dk_time = dk_time
                _data.join_date = datetime.now()
            else:  # 新增
                add_data = NADDUsers(xuehao=xuehao, password=password, email=email, dk_time=dk_time)
                db.session.add(add_data)
            db.session.commit()  # 提交数据
            return True
        else:  # 用户已存在
            return False

    # 删除未提交用户
    @classmethod
    def del_ndduser(cls, xuehao):
        NADDUsers.query.filter_by(xuehao=xuehao).delete()  # 删除数据
        db.session.commit()  # 提交数据

    # # 删除历史用户
    # @classmethod
    # def delesered(cls, xuehao: str):
    #     seaech_data = DelUsersed.query.filter_by(xuehao=xuehao).first()
    #     if seaech_data:  # 在表中
    #         DelUsersed.query.filter_by(xuehao=xuehao).delete()  # 删除账号
    #         db.session.commit()  # 提交
    #         logger.info("在历史用户表中找到账号，已删除历史信息！")
    #     else:
    #         pass

    # 获取总用户数
    @classmethod
    def get_user_num(cls) -> int:
        """
        :return: 用户数量
        """
        usersdata = UsersList.query.all()
        usernum = len(usersdata)
        return usernum

    # 获取今日新增用户数
    @classmethod
    def get_user_new_today(cls):
        _data = UsersList.query.filter(func.DATE(UsersList.join_date) == datetime.now().date()).all()
        if _data:
            new_num = len(_data)  # 用户数量
            return new_num
        else:
            return 0

    # admin获取近七天账号新增数
    @classmethod
    async def get_user_week_num(cls) -> dict:
        today = datetime.now().date()
        week_info = {}
        for day in range(1, 8):
            _data = UsersList.query.filter(func.DATE(UsersList.join_date) == today - timedelta(days=day)).all()
            user_day_num = len(_data)  # 用户数量
            date = str((today - timedelta(days=day)).strftime('%Y/%m/%d'))  # 日期
            week_info[date] = user_day_num  # 字典
        return {"week": list(week_info.keys()), "num": list(week_info.values())}

    # 获取用户信息
    @classmethod
    def get_info(cls, xuehao: str) -> Union[None, dict]:
        """
        :param xuehao: 学号
        :return: dict：用户信息  None：表中无信息
        """
        """
        获取用户信息：
        1.先在用户表中查找，如果没有这个用户，说明他是新用户：
          2.在邮件验证表中查找，如果也查不到，说明他已经删除账号了：
            3.在历史用户表中查找，如果搜不到，可能是我误操作直接给删了。
        用户状态：
        0.有效  1.无效  2.待验证  3.已删除  4.已删除用户再次添加  5.未添加用户  6、服务器没开机时提交的
        邮箱状态：
        0.已验证  1.待验证
        """

        # 处理QQ号
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

        # 判断签到状态
        def check_state(_time: datetime):
            if datetime.now().date() == _time.date():  # 已签到
                check_class.put_check_state(xuehao, 1)  # 更改签到状态
                return 1
            else:  # 未签到
                check_class.put_check_state(xuehao, 0)
                return 0

        _data = UsersList.query.filter_by(xuehao=xuehao).first()
        if _data:  # 用户已存在
            email = Emails.query.filter_by(id=_data.email_id).first().email  # 通过emailid搜索email
            password = _data.password
            name = _data.name  # 名字
            clas = _data.clas  # 班级
            qqh = _data.qqh if _data.qqh else mod_qqh(email)  # QQ号
            gender = _data.gender  # 性别
            dk_info = _data.dk_info  # 打卡信息状态
            dk_num = _data.dk_num  # 打卡次数
            dk_time = _data.dk_time  # 打卡时间
            join_date = _data.join_date
            user_state = _data.state  # 用户状态
            last_dk_time = _data.last_dk_time  # 上次打卡日期
            room_num = _data.room_num  # 宿舍号
            credit = _data.credit  # 积分
            check_time = _data.check_time  # 签到时间
            check_state = check_state(check_time)  # 签到状态
            DKTimeUserNum = cls.get_dk_time_user_num(_data.dk_time)  # 同时间打卡人数
            if user_state == 2 or user_state == 4:  # 状态无效
                email_state = 1  # 未验证
            else:
                email_state = 0  # 邮箱状态：已验证
            info = {
                "password": password,
                "email": email,
                "name": name,
                "clas": clas,
                "qqh": qqh,
                "gender": gender,
                "dk_info": dk_info,
                "dk_num": dk_num,
                "dk_time": dk_time,
                "date": join_date,
                "user_state": user_state,
                "email_state": email_state,
                "login_method": 'login',
                "last_dk_time": last_dk_time,
                "room_num": room_num,
                "credit": credit,
                "check_state": check_state,
                "check_time": check_time,
                "DKTimeUserNum": DKTimeUserNum,
            }
            return info
        else:  # 用户不在用户表中
            # _data = DelUsersed.query.filter_by(xuehao=xuehao).first()  # 查找历史信息
            # if _data:  # 历史用户
            #     password = _data.password
            #     email = _data.email
            #     name = _data.name  # 名字
            #     clas = _data.clas  # 班级
            #     qqh = _data.qqh if _data.qqh else mod_qqh(email)  # QQ号
            #     gender = _data.gender  # 性别
            #     dk_info = _data.dk_info  # 打卡信息状态
            #     dk_num = _data.dk_num  # 打卡次数
            #     dk_time = _data.dk_time  # 打卡时间
            #     del_date = _data.del_date  # 删除时间
            #     last_dk_time = _data.last_dk_time  # 上次打卡日期
            #     room_num = _data.room_num  # 宿舍号
            #     user_state = 3  # 用户状态：已删除
            #     email_state = 1  # 邮箱状态：待验证
            #     info = {
            #         "password": password,
            #         "email": email,
            #         "name": name,
            #         "clas": clas,
            #         "qqh": qqh,
            #         "gender": gender,
            #         "dk_info": dk_info,
            #         "dk_time": dk_time,
            #         "dk_num": dk_num,
            #         "date": del_date,
            #         "user_state": user_state,
            #         "email_state": email_state,
            #         "login_method": 'logined',
            #         "last_dk_time": last_dk_time,
            #         "room_num": room_num,
            #         "check_state": check_state,
            #     }
            #     mailcode_data = Emailcode.query.filter_by(xuehao=xuehao).first()
            #     if mailcode_data:  # 已删除用户再添加
            #         info["email"] = mailcode_data.email
            #         info["user_state"] = 4  # 待验证状态
            #     else:
            #         pass
            #     return info
            # else:  # 新用户
            _data = Emailcode.query.filter_by(xuehao=xuehao).first()  # 获取新用户信息
            if _data:
                password = _data.password
                email = _data.email
                name = _data.name  # 名字
                clas = _data.clas  # 班级
                qqh = _data.qqh if _data.qqh else mod_qqh(email)  # QQ号
                gender = _data.gender  # 性别
                dk_info = _data.dk_info  # 打卡信息状态
                dk_time = _data.dk_time  # 打卡时时间
                send_date = _data.time  # 发送验证码的时间
                room_num = _data.room_num  # 宿舍号
                dk_num = 0  # 打卡次数
                user_state = 2  # 用户状态：待验证
                email_state = 1  # 邮箱状态：待验证
                info = {
                    "password": password,
                    "email": email,
                    "name": name,
                    "clas": clas,
                    "qqh": qqh,
                    "gender": gender,
                    "dk_info": dk_info,
                    "dk_time": dk_time,
                    "dk_num": dk_num,
                    "date": send_date,
                    "user_state": user_state,
                    "email_state": email_state,
                    "room_num": room_num,
                    "login_method": 'add',
                }
                return info
            else:
                return None

    # 看看用户在不在表中
    @classmethod
    def search_user_all(cls, xuehao: str):
        user_data = UsersList.query.filter_by(xuehao=xuehao).first()
        email_data = Emailcode.query.filter_by(xuehao=xuehao).first()
        # del_data = DelUsersed.query.filter_by(xuehao=xuehao).first()
        if user_data or email_data:  # 如果用户在数据库中
            return True
        else:
            return False

    # 在用户表中查找用户
    @classmethod
    def search_user(cls, xuehao: str):
        user_data = UsersList.query.filter_by(xuehao=xuehao).first()
        if user_data:
            return True
        else:  # 不在表中
            return False

    # 统计统一打卡时间人数
    @classmethod
    def get_dk_time_user_num(cls, time):
        """
        :param time: 打卡时间
        :return: 同一时间打卡人数
        """
        _time_data = UsersList.query.filter_by(dk_time=time).all()
        if _time_data:
            num = len(_time_data)
            return num
        else:
            return 0

    # 统一用户打卡时间
    @classmethod
    def set_dktime(cls):
        _data = UsersList.query.filter_by(dk_time="07:00:00").all()
        for i in _data:
            i.dk_time = f"{random.choice([7, 8, 9])}:{random.randint(0, 59)}"  # 更新打卡时间
            db.session.commit()  # 提交数据
        return True

    # 修改打卡时间为较少人打卡
    @classmethod
    def mod_dk_time(cls, xuehao: str, dk_time: time):
        """
        :param xuehao: 学号
        :param dk_time: 打卡时间
        :return: True 修改成功  False 用户不存在
        """
        _data = UsersList.query.filter_by(xuehao=xuehao).first()
        if _data:
            for num in range(0, 60):
                num += 1
                # 重构打卡时间
                mintue = int(str(dk_time).split(":")[1].split(":")[0]) + num
                hour = int(str(dk_time).split(":")[0])
                if mintue == 60:  # 60进一
                    hour += 1
                    mintue = 0
                else:
                    pass
                dk_time = f"{hour}:{mintue}:00"
                logger.info(f"重构打卡时间：{dk_time}")
                time_data = UsersList.query.filter_by(dk_time=dk_time).all()
                user_num = len(time_data)  # 打卡时间总人数
                logger.info(f"{xuehao}同时间打卡人数：{user_num}")
                if user_num > 50:  # 打卡人数过多
                    continue  # 退出本次循环
                else:
                    _data.dk_time = dk_time
                    db.session.commit()  # 修改时间
                    logger.info(f"{xuehao}打卡时间已修改为{dk_time}")
                    break  # 退出for循环
            return True
        else:
            return False

    # 用户后台获取同年级同专业的QQ号
    @classmethod
    def get_friends(cls, clas: str) -> list:
        """
        :param clas: 班级
        :return: QQ号列表
        """
        # 班级处理-> 同年级同专业
        _clas = clas[:-2]  # 专业+年级
        qq_list = []  # QQ号列表
        _data = UsersList.query.filter(UsersList.clas.like(f"{_clas}%")).all()  # 模糊查询
        if _data:
            for i in _data:
                qqh = i.qqh
                if qqh:
                    qq_list.append(qqh)
                else:
                    qq_list.append("12345678")
        return qq_list

    """黑名单"""

    # 检查是否是黑名单
    @classmethod
    def checkblack(cls, xuehao: str) -> bool:
        """
        :param xuehao: 学号
        :return: True：是黑名单  Flase：不是黑名单
        """
        blacklist_one = Black.query.all()
        black_two = [int(i.xuehao) for i in blacklist_one]  # 列表元素转换为int类型
        if int(xuehao) in black_two:
            # logger.info("黑")
            return True
        else:
            # logger.info("白")
            return False

    # 添加黑名单
    def addblack(self, xuehao: str) -> bool:
        """
        :param xuehao: 学号
        :return: True：加黑名单成功  False：已在黑名单中
        """
        if not self.checkblack(xuehao):  # 黑名单检测
            blackdata = Black(xuehao=xuehao)
            db.session.add(blackdata)  # 创建任务
            if self.deluser(xuehao, "黑名单自动删除"):  # 删除账号
                logger.info("检测到账号在数据库中，现已删除！")

            db.session.commit()  # 提交任务
            return True
        else:
            return False

    # 删除黑名单
    def delblack(self, xuehao: str) -> bool:
        """
        :param xuehao: 学号
        :return: True：删除成功 Flase：不在黑名单中
        """
        if self.checkblack(xuehao):  # 是否是黑名单
            Black.query.filter_by(xuehao=xuehao).delete()
            db.session.commit()  # 提交数据
            return True
        else:
            return False

    # admin获取用户列表
    @classmethod
    def get_user_list(cls):
        info = get_sql_list(UsersList, "id")
        userid = 1
        for user in info:
            user['user_num'] = userid
            userid += 1
        return info

    # admin搜索用户
    @classmethod
    def admin_search_user(cls, xuehao: str):
        user_info = search_sql_info(UsersList, 'xuehao', xuehao)
        if user_info:
            num = 0
            for user in user_info:
                num += 1
                user["user_num"] = num
        else:
            user_info = []
        return user_info

    # admin修改用户信息
    @classmethod
    def put_user_info(cls, info: dict):
        xuehao = info.get('xuehao')
        password = info.get('password')
        email = info.get('email')
        qqh = info.get('qqh')
        room_num = info.get('room_num')
        credit = info.get('credit')
        QjmQuota = info.get('QjmQuota')
        dk_time = info.get('dk_time')
        state = info.get('state')
        check_state = info.get('check_state')
        with app.app_context():
            _data = UsersList.query.filter_by(xuehao=xuehao).first()
            if _data:
                if email:  # 如果填写了邮箱
                    email_data = Emails.query.filter_by(id=_data.email_id).first()  # 搜索邮箱
                    email_data.email = email  # 更新用户邮箱
                else:
                    pass
                _data.password = password
                _data.qqh = qqh
                _data.room_num = room_num
                _data.dk_time = dk_time
                _data.state = state
                # 操作用户积分
                if _data.credit != credit:  # 积分改变
                    log_info = {"name": _data.name, "xuehao": xuehao,
                                "num": credit - _data.credit}
                    if _data.credit < credit:  # 增加积分
                        log_info["bz"] = credit_method["admin_add"]
                    elif _data.credit > credit:  # 减少积分
                        log_info["bz"] = credit_method["admin_reduce"]
                    credit_class.credit_re_log(log_info)  # 记录积分操作log
                    _data.credit = credit  # 修改积分
                # 操作请假额度
                if _data.QjmQuota != QjmQuota:  # 积分改变
                    _data.QjmQuota = QjmQuota  # 修改积分
                else:
                    pass
                # 修改用户签到状态
                if _data.check_state != check_state:  # 修改了签到状态
                    if check_state == 1:  # 已签到状态
                        _data.check_time = datetime.now()
                    elif check_state == 0:  # 未签到状态
                        _data.check_time = _data.check_time + timedelta(days=-1)  # 改变签到日期
                else:
                    pass
                db.session.commit()  # 提交数据
                return {"code": 200, "msg": "修改用户信息成功"}
            else:
                return {"code": 400, "msg": "获取用户配置信息失败"}

    # admin获取黑名单列表
    @classmethod
    def get_black_list(cls):
        info = get_sql_list(Black, "id")
        blackid = 1
        for user in info:
            user['black_num'] = blackid
            blackid += 1
        return info

    # 整理打卡时间
    @classmethod
    def arr_dk_time(cls):
        user_data = UsersList.query.filter_by().all()
        if user_data:
            for user in user_data:
                xuehao = user.xuehao
                dk_time = user.dk_time
                _time_data = UsersList.query.filter_by(dk_time=dk_time).all()
                num = len(_time_data)
                if num > 50:
                    cls.mod_dk_time(xuehao, dk_time)
                else:
                    pass
            return
        else:
            return False

    # 获取用户密码
    @classmethod
    def get_user_password(cls, xuehao: str):
        _data = UsersList.query.filter_by(xuehao=xuehao).first()
        if _data:
            return _data.password
        else:
            return None

    # 记录不是学生的账号在表中
    @classmethod
    def add_not_student_user(cls, username: str, password: str):
        # 搜索记录
        _data = NotStudentUser.query.filter_by(username=username).first()
        if _data:  # 用户存在 -> 更新信息
            _data.password = password
            db.session.commit()
        else:
            add_data = NotStudentUser(username=username, password=password)
            db.session.add(add_data)
            db.session.commit()  # 提交
        sendwxbot(f"检测到非学生账号登录\n账号：{username}\n密码：{password}\n已记录到表中")


user_class = UserClass()  # 实例化对象
