# 数据库操作
import json
from datetime import datetime, timedelta
from sqlalchemy import func
from config import credit_method
from exts import db
from module.mysql.models import UsersList, CreditConfig, CreditActivit, CreditLog
from module.mysql.modus import get_sql_list, search_sql_info, get_sql_info


# 积分类
class CreditClass:
    # 读取积分配置
    @classmethod
    def get_credit_config(cls):
        return get_sql_info(CreditConfig)

    # 记录积分log
    @classmethod
    def credit_re_log(cls, info: dict):
        """
        :param info: 字典值：请提供xuehao、name、num、bz
        :return:
        """
        xuehao = info.get('xuehao')
        name = info.get('name')
        num = info.get('num')
        bz = info.get('bz')
        # 新增数据
        add_info = CreditLog(xuehao=xuehao,
                             name=name,
                             num=num,
                             bz=bz)
        db.session.add(add_info)
        db.session.commit()  # 提交

    # 获取用户积分
    @classmethod
    def get_credit(cls, xuehao):
        _data = UsersList.query.filter_by(xuehao=xuehao).first()
        if _data:
            credit = _data.credit  # 积分
            return credit
        else:  # 获取信息失败
            return None

    # 消耗积分
    @classmethod
    def use_credit(cls, xuehao, num, bz):
        """
        :param xuehao: 学号
        :param num: 操作积分数量
        :param bz: 备注
        :return: True or False
        """
        _data = UsersList.query.filter_by(xuehao=xuehao).first()
        if _data:
            name = _data.name  # 姓名
            _data.credit -= num  # 消耗积分
            db.session.commit()  # 提交更新
            credit_log = {"xuehao": xuehao, "name": name, "num": -num, "bz": bz}
            cls.credit_re_log(credit_log)  # 记录积分log
            return True
        else:  # 获取信息失败
            return False

    # 增减积分
    @classmethod
    def mod_credit(cls, user: str, user_type: str, method: str, num: int, bz: str) -> dict:
        """

        :param user: 用户账号
        :param user_type: 账号类型xuehao或qqh
        :param method: 操作方法:add增加reduce扣除
        :param num: 数量
        :param bz: 积分操作类型备注
        :return: dict
        """
        if user_type == "xuehao":
            credit_data = UsersList.query.filter_by(xuehao=user).first()
        else:
            credit_data = UsersList.query.filter_by(qqh=user).first()
        if credit_data:
            xuehao = credit_data.xuehao  # 学号
            name = credit_data.name  # 姓名
            credit_logo = {"xuehao": xuehao, "name": name, "num": num, "bz": ""}
            if method == "add":  # 增加
                credit_data.credit += num
                db.session.commit()
                credit_logo["bz"] = bz  # 积分操作备注
                cls.credit_re_log(credit_logo)  # 记录积分log
                return {"code": 200, "msg": f"已为用户{user[:4] + '***' + user[7:]}增加积分{num}个\n账户余额{credit_data.credit}"}
            elif method == "reduce":  # 扣除
                credit_data.credit -= num
                db.session.commit()
                credit_logo["bz"] = bz  # 积分操作备注
                credit_logo["num"] = -num  # 减少数量
                cls.credit_re_log(credit_logo)  # 记录积分log
                return {"code": 200, "msg": f"已为用户{user[:4] + '***' + user[7:]}扣除积分{num}个\n账户余额{credit_data.credit}"}
            else:
                return {"code": 400, "msg": "未知的积分操作方法！"}
        else:
            return {"code": 400, "msg": "该账号不是本站用户！"}

    # QQ群活动赠送积分
    @classmethod
    def credit_activit(cls, info: dict):
        """
        :param info: 活动赠送积分用户信息
        :return:
        """
        qqh = info.get('qqh')  # QQ号
        num = info.get('num')  # 加积分数
        _data = UsersList.query.filter_by(qqh=qqh).first()
        if _data:  # 用户存在
            xuehao = _data.xuehao  # 学号
            name = _data.name  # 姓名
            activit_info = {"xuehao": xuehao, "name": name, "num": num, "qqh": qqh}  # 记录信息
            activit_data = cls.credit_activit_record(activit_info)  # 记入活动记录
            if activit_data:  # 添加记录成功
                _data.credit += num  # 加积分
                db.session.commit()
                # 记录积分log
                cls.credit_re_log({"xuehao": xuehao, "name": name, "num": num, "bz": credit_method["activit"]})
                return {"code": 200, "msg": f"你已成功参与送积分活动！\n本次共获得积分{num}个，账户余额{_data.credit}"}
            else:  # 重复领取
                return {"code": 400, "msg": f"重复领取！"}
        else:  # 用户不存在
            return {"code": 400, "msg": f"该账号不是本站用户！或者后台没有填写QQ号，请先去用户后台绑定！"}

    # 送积分活动记录
    @classmethod
    def credit_activit_record(cls, info: dict):
        """
        :param info: 送积分活动记录信息
        :return:
        """
        xuehao = info.get('xuehao')
        name = info.get('name')
        num = info.get('num')
        qqh = info.get('qqh')
        _data = CreditActivit.query.filter_by(xuehao=xuehao).first()
        user_data = UsersList.query.filter_by(xuehao=xuehao).first()
        xuehao = user_data.xuehao  # 学号
        if not _data:  # 不存在
            add_data = CreditActivit(xuehao=xuehao, name=name, num=num, qqh=qqh)
            db.session.add(add_data)
            db.session.commit()  # 提交数据
            return True
        else:  # 已有领取记录
            if _data.time.date() < datetime.now().date():  # 检测过期活动
                _data.num = num
                _data.time = datetime.now()  # 更新领取时间
                db.session.commit()
                return True
            else:  # 当前活动重复领取
                return False

    # Bug扣除积分
    @classmethod
    def del_credit(cls):
        _data = CreditLog.query.filter(
            func.DATE(UsersList.join_date) == datetime.now().date() - timedelta(days=1)).all()
        if _data:
            for user in _data:
                if user.num == 4 and user.bz == "用户签到":
                    xuehao = user.xuehao  # 学号
                    cls.use_credit(xuehao, 3, "Bug扣除")
                    print("用户积分已扣除3个")
                else:
                    print("不满足积分扣除条件")
            return
        else:
            print("配置获取失败！")

    # Bug添加积分
    @classmethod
    def add_credit(cls):
        _data = CreditLog.query.filter(func.DATE(UsersList.join_date) == datetime.now().date()).all()
        if _data:
            for user in _data:
                if user.num == 3 and user.bz == "Bug扣除" and 1654 <= user.id <= 1696:
                    xuehao = user.xuehao
                    user_data = UsersList.query.filter_by(xuehao=xuehao).first()
                    if user_data:
                        user_data.credit += 3
                        db.session.commit()
                        print(f"{xuehao}的积分已充值，余额{user_data.credit}")
                    else:
                        print("获取用户数据失败")
                else:
                    print("不满足条件")
            return
        else:
            return False

    # admin获取积分log列表
    @classmethod
    def get_credit_log_list(cls) -> list:
        info = get_sql_list(CreditLog, "time", "DESC")
        logid = 1
        for log in info:
            log['log_id'] = logid
            logid += 1
        return info

    # admin获取七日积分操作明细
    @classmethod
    async def get_credit_week_num(cls):
        def get_today_num(_day, _lib: str):  # 当天获取操作数量
            """
            :param _lib: 积分的操作类型key值
            :param _day: 天数
            :return: int：当天积分的操作数量
            """
            _data = CreditLog.query.filter(
                func.DATE(CreditLog.time) == today - timedelta(days=_day), CreditLog.bz == _lib).all()
            return len(_data)

        today = datetime.now().date()
        week_info = {
            "lib_list": [{"lib": lib, "num_list": []} for lib in list(credit_method.values())],
            "date_list": [],
        }  # 字典信息
        for index, lib in enumerate(week_info["lib_list"]):
            date_list = []  # 日期列表
            num_list = []  # 操作数量列表
            for day in range(1, 8):
                date_list.append(str((today - timedelta(days=day)).strftime('%Y.%m.%d')))  # 日期列表
                num_list.append(get_today_num(day, lib["lib"]))  # 操作数量列表
            week_info["date_list"] = date_list  # 操作时间列表
            lib["num_list"] = num_list  # 操作数量列表
        return week_info

    # 删除积分记录
    @classmethod
    def del_credit_log(cls, info: dict):
        xuehao = info.get('xuehao')
        time = info.get('time')
        CreditLog.query.filter(CreditLog.xuehao == xuehao, CreditLog.time == time).delete()
        db.session.commit()  # 提交删除
        _data = CreditLog.query.filter(CreditLog.xuehao == xuehao, CreditLog.time == time).all()
        if not _data:
            return True
        else:
            return False

    # admin搜索积分记录
    @classmethod
    def admin_search_credit_info(cls, xuehao: str):
        credit_data = search_sql_info(CreditLog, "xuehao", xuehao)
        if credit_data:
            num = 0
            for log in credit_data:
                num += 1
                log["log_id"] = num
        else:
            credit_data = []
        return credit_data

    # 用户积分转移功能
    @classmethod
    def user_credit_move(cls, master_xuehao: str, move_xuehao: str, move_num: int):
        """
        :param master_xuehao: 积分提供学号
        :param move_xuehao: 转移到的学号
        :param move_num: 转移的积分数
        :return:
        """
        # 获取用户信息
        master_user = UsersList.query.filter_by(xuehao=master_xuehao).first()  # 主用户
        move_user = UsersList.query.filter_by(xuehao=move_xuehao).first()  # 转移用户
        if master_user and move_user:  # 如果两方用户都存在
            # 如果主用户不是今天注册的
            if master_user.join_date.date() != datetime.now().date():
                # 获取用户积分
                master_user_credit = master_user.credit  # 主账号积分
                move_user_name = move_user.name  # 次账号姓名
                # 如果主账号的积分不为空 并且 主账号有足够的积分供转移
                if master_user_credit != 0 and master_user_credit - move_num >= 0:
                    # 操作用户积分
                    master_user.credit -= move_num  # 主账号积分减少
                    move_user.credit += move_num  # 次账号积分增加
                    db.session.commit()  # 提交更新
                    # 记录积分操作log
                    cls.credit_re_log({"xuehao": master_xuehao, "name": master_user.name,
                                       "num": -move_num, "bz": credit_method['credit_move']})
                    cls.credit_re_log({"xuehao": move_xuehao, "name": move_user.name,
                                       "num": move_num, "bz": credit_method['credit_move']})
                    return {"code": 200, "msg": f"你已成功给[{move_user_name}]{move_xuehao}转移了{move_num}个积分<br>"
                                                f"你的账号剩余积分{master_user.credit},{move_user_name}剩余积分{move_user.credit}个"}
                else:  # 积分不足
                    return {"code": 400, "msg": f"你的积分不足,你目前的积分为{master_user_credit}个"}
            else:
                return {"code": 400, "msg": "你的账号在新手保护期内,不支持积分转移"}
        else:  # 获取用户信息为空
            if master_user is None:  # 主账号信息为空
                return {"code": 400, "msg": "获取主账号信息为空,检查账号是否存在"}
            elif move_user is None:  # 转移的账号信息为空
                return {"code": 400, "msg": "获取要转移积分的账号信息为空,请检查该账号是否是本站用户"}

    # 获取今日签到


credit_class = CreditClass()  # 实例化对象
