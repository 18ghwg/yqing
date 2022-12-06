from datetime import datetime
from exts import app, db
from module import send_email
from module.mysql import UsersList, Emailcode, Emails, NotDKUsers
from config import logger


# 读取用户信息
async def get_user_info(xuehao: str):
    with app.app_context():
        _data = UsersList.query.filter_by(xuehao=xuehao).first()
        name = _data.name  # 姓名
    info = {
        "name": name,
        "xuehao": xuehao,
        "xhxm": f"[{xuehao}]{name}"  # [学号]姓名
    }
    return info


# 修改用户状态
async def modstate(xuehao: str, abled: str):
    """
    :param xuehao: 学号
    :param abled: enabled：启用、disabled：禁用
    :return: str: 操作状态
    """
    able = 0  # 状态码
    if abled == "enabled":  # 启用
        able = 0
    elif abled == "disabled":  # 禁用
        able = 1
    # 修改
    with app.app_context():
        _data = UsersList.query.filter_by(xuehao=xuehao).first()
        _data.state = able  # 更新状态
        db.session.commit()  # 提交数据
        logger.info(f"{abled}成功")
        return f"{abled}成功"


# 删除用户
async def deluser(xuehao: str):
    with app.app_context():
        _data = UsersList.query.filter_by(xuehao=xuehao).first()
    email_id = _data.email_id
    with app.app_context():
        _email_data = Emails.query.filter_by(id=email_id).first()
    email = _email_data.email
    with app.app_context():
        UsersList.query.filter_by(xuehao=xuehao).delete()
        Emails.query.filter_by(email=email).delete()
        db.session.commit()  # 提交删除
    logger.info(f"无效账号{xuehao}删除成功！")
    # 邮件提醒
    await send_email(email, f"检测到你的账号{xuehao}状态无效<br>现已删除！", "账号删除提醒")


# 增加打卡次数
async def dk_nums(xuehao: str):
    with app.app_context():
        _data = UsersList.query.filter_by(xuehao=xuehao).first()
        dk_num = _data.dk_num  # 获取打卡次数
        _data.dk_num = dk_num + 1
        _data.last_dk_time = datetime.now()  # 更新打卡日期
        db.session.commit()  # 提交
        dk_num += 1
    logger.info("打卡次数获取成功！")
    return f"你在本站成功打卡{dk_num}次<br>更多信息可登录用户后台查看！"


# 添加未及时打卡的用户到表中
async def up_ndkuser(xuehao: str, password: str, email_id: int, state: int):
    with app.app_context():
        _data = NotDKUsers.query.filter_by(xuehao=xuehao).all()
        if not _data:
            _ndkdata = NotDKUsers(xuehao=xuehao, password=password, email_id=email_id, state=state)  # 把未打卡账号加到表中
            logger.info(f"已将{xuehao}加入未打卡用户列表！")
            db.session.add(_ndkdata)  # 添加
            db.session.commit()  # 提交
        else:
            logger.info("未打卡用户已存在，不能重复添加")


# 获取未打卡用户列表
async def get_ndkusers() -> list:
    with app.app_context():
        _data = NotDKUsers.query.filter_by().all()
        if _data:
            logger.info("获取未打卡用户列表成功！")
    return _data


# 删除未打卡用户
async def del_ndkuser(xuehao: str):
    with app.app_context():
        _data = NotDKUsers.query.filter_by(xuehao=xuehao).first()
        if _data:  # 存在->删除
            with app.app_context():
                NotDKUsers.query.filter_by(xuehao=xuehao).delete()  # 删除
                db.session.commit()  # 提交
            logger.info(f"未打卡用户：{xuehao}已从表中删除！")
        else:
            pass


# 设置用户打卡信息状态
async def set_dk_info_state(xuehao: str, mode: int):
    """
    :param xuehao: 账号
    :param mode: 0：获取历史信息为空  1：正常
    :return:
    """
    with app.app_context():
        info_data = UsersList.query.filter_by(xuehao=xuehao).first()
        info_data.dk_info = mode  # 设置打卡转态为
        db.session.commit()  # 提交数据
