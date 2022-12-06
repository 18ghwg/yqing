# 数据库操作
from datetime import datetime
from config import credit_method
from exts import db
from module.mysql import UsersList
from module.mysql.CreditClass import credit_class


# 签到类
class CheckClass:
    # 用户签到
    @classmethod
    def user_check(cls, xuehao):
        check_data = UsersList.query.filter_by(xuehao=xuehao).first()
        credit_config = credit_class.get_credit_config()  # 获取积分配置
        if credit_config:
            CheckCredit = credit_config["CheckCredit"]  # 签到获取积分数
            if check_data:  # 用户存在
                name = check_data.name  # 姓名
                credit = check_data.credit  # 当前积分
                check_state = check_data.check_state  # 签到状态bool
                check_time = check_data.check_time  # 签到时间
                today = datetime.now()  # 今天的日期
                if check_state == 0 and today.date() > check_time.date():  # 今日未签到
                    check_data.check_state = 1  # 签到状态
                    check_data.check_time = today  # 签到时间
                    check_data.credit = credit + CheckCredit  # 加积分
                    db.session.commit()  # 更新数据
                    credit_class.credit_re_log({"xuehao": xuehao, "name": name,
                                                "num": CheckCredit, "bz": credit_method["user_check"]})
                    return {"code": 200, "msg": f"签到成功！获得积分{check_data.credit - credit}个！"}
                else:  # 今日已签到
                    return {"code": 400, "msg": "今日已签到"}
            else:  # 用户不存在
                return {"code": 400, "msg": "用户不存在！"}
        else:
            return {"code": 400, "msg": "获取积分配置失败！"}

    # 修改签到状态
    @classmethod
    def put_check_state(cls, xuehao, state):
        _data = UsersList.query.filter_by(xuehao=xuehao).first()
        _data.check_state = state
        db.session.commit()  # 更新数据


check_class = CheckClass()  # 实例化对象
