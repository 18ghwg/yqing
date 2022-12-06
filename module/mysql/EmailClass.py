# 数据库操作
from config import logger
from exts import db, app
from module.mysql import UsersList, Emails, Emailcode, Config


# 邮件类
class EmailClass:
    # 删除邮箱验证码
    @classmethod
    def delemailcode(cls, email: str) -> bool:
        """
        :param email: 邮箱
        :return: True：删除成功  False：信息不存在/删除失败
        """
        deldata = Emailcode.query.filter_by(email=email).first()
        if deldata:
            Emailcode.query.filter_by(email=email).delete()  # 删除
            db.session.commit()  # 提交
            emailcodedata = Emailcode.query.filter_by(email=email).first()
            if not emailcodedata:  # 再次查询在没在表中
                return True
            else:
                return False
        else:  # 没搜到信息
            return False

    # 设置邮件公告内容
    @classmethod
    def put_email_gg(cls, content: str):
        """
        :param content: 邮件公告内容
        :return: True：设置成功  Fasle：设置失败
        """
        maildata = Config.query.filter_by(id=1)[0]
        maildata.EmailGG = content
        db.session.commit()  # 提交数据
        ggdata = Config.query[0].EmailGG  # 当前公告内容
        if ggdata == content:
            return True
        else:
            return False

    # 获取验证邮件最大发送次数
    @classmethod
    def get_sendemail_maxnum(cls) -> int:
        """
        :return: 邮箱验证的最大发送邮件数量
        """
        getnumdata = Config.query.filter_by(id=1)[0]
        if getnumdata:
            maxnum = int(getnumdata.SendEmailMaxNum)
            return maxnum
        else:
            return 10

    # 修改邮件最大发送次数
    @classmethod
    def set_sendemail_maxnumber(cls, number: int):
        """
        :param number: 最大次数数值
        :return: True：修改成功  False：修改失败未搜到id=1的config数据
        """
        putdata = Config.query.filter_by(id=1).first()
        if putdata:
            putdata.SendEmailMaxNum = number  # 修改数值
            db.session.commit()  # 提交数据
            return {"code": 200, "message": f"疫情打卡web：\n邮件最大验证次数已设置为{number}"}
        else:
            return {"code": 400, "message": f"疫情打卡web：\n没有在数据库中找到配置！"}

    # 清除邮件验证次数
    @classmethod
    def clear_sendnumber(cls, email: str):
        """
        :param email: 邮箱
        :return: 两种状态：1、成功清零 2、没有找到这条数据
        """
        cleardata = Emailcode.query.filter_by(email=email).first()
        if cleardata:
            cleardata.send_num = 0  # 清零
            db.session.commit()  # 提交数据
            return {"code": 200, "message": f"疫情打卡web：\n邮箱{email}下的验证次数已清零！"}
        else:
            return {"code": 400, "message": f"疫情打卡web：\n未找到邮箱{email}当前的验证信息！"}

    # 检查邮箱是否存在
    @classmethod
    def checkemail(cls, email: str) -> bool:
        """
        :param email: 邮箱
        :return: True: 存在  False：不存在
        """
        check_data = Emails.query.filter_by(email=email).first()
        if check_data:  # 邮箱已存在
            check_data = Emails.query.filter_by(email=email).first()  # 第二次查询
            if check_data:
                email_id = check_data.id  # 获取emailid
                data_state = UsersList.query.filter_by(email_id=email_id).first()  # 获取用户表中的状态
                if data_state:  # 获取到用户数据
                    state = data_state.state  # 获取状态码
                    if state == 1:  # 账号无效视作更新提交
                        return False
                    else:  # 账号有效视作重复提交
                        return True
                else:  # 没有获取到数据
                    return False
            else:
                return False
        else:  # 邮箱不存在
            return False

    # 邮箱查重2
    @classmethod
    def check_email2(cls, email: str, xuehao: str):
        """
        :param email:   邮箱
        :param xuehao:  学号
        :return: True：邮箱被占用  False：检查通过
        """
        _data = Emails.query.filter_by(email=email).first()
        if _data:  # 如果邮箱没改变：通过旧邮箱搜索
            email_id = _data.id  # 邮箱id
            _user = UsersList.query.filter_by(email_id=email_id).first()  # 搜索对应的用户
            _xuehao = _user.xuehao  # 获取当前邮箱下的学号
            if _xuehao == xuehao:  # 用户邮箱没有改变
                return False
            else:  # 邮箱被占用
                return True
        else:  # 邮箱改变了
            mailcode_data = Emailcode.query.filter_by(xuehao=xuehao).first()
            if mailcode_data:  # 如果在验证码表中
                return "待验证"
            else:  # 已提交用户改变邮箱
                # 更改用户状态为待验证
                _user = UsersList.query.filter_by(xuehao=xuehao).first()  # 搜索用户
                _user.state = 2  # 更改用户状态为待验证
                db.session.commit()  # 提交数据
                return "待验证"

    # 记录用户拒收邮件次数
    @classmethod
    def email_re_send_fail_num(cls, xuehao, num):
        with app.app_context():
            user_data = UsersList.query.filter_by(xuehao=xuehao).first()
            if user_data:  # 获取到数据
                user_data.send_fail_num += num  # 发送失败数加一
                db.session.commit()  # 提交数据
                logger.info(f"邮件拒收数量加{num}\n{xuehao}的邮件拒收数量为{user_data.send_fail_num}")
                return True
            else:  # 未获取到数据
                return False

    # 获取邮件做大拒收数量
    @classmethod
    def email_get_fial_max_num(cls):
        config = Config.query.get(1)  # 获取网站配置信息
        if config:  # 获取成功
            return config.SendFailMaxNum  # 发送失败的最大数量
        else:  # 获取失败-> 使用默认值
            return 3

    # 检测邮件拒收数是否超过限制
    @classmethod
    def email_check_send_fail_num(cls, xuehao):
        with app.app_context():
            user_data = UsersList.query.filter_by(xuehao=xuehao).first()
            if user_data:  # 获取到数据
                email_user_send_fail_num = user_data.send_fail_num  # 用户的邮件拒收数量
                SendFailNumMax = cls.email_get_fial_max_num()  # 设置的最大拒收数量限制
                if email_user_send_fail_num >= SendFailNumMax:  # 用户拒收数量超过限定的最大值
                    logger.info(f"{xuehao}的邮件拒收数量超过最大限制{SendFailNumMax}")
                    return True
                else:  # 未超过最大数量
                    return False
            else:  # 未获取到用户信息
                return False


email_class = EmailClass()  # 实例化对象
