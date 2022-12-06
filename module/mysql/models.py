from exts import db
from datetime import datetime


# 邮箱表
class Emails(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False, unique=True, comment="用户邮箱")
    __mapper_args__ = {
        "order_by": id  # -id
    }


# 管理员列表
class Admins(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    xuehao = db.Column(db.String(50), nullable=False, unique=True, comment="学号")
    password = db.Column(db.String(20), nullable=False, comment="密码")


# 用户表
class UsersList(db.Model):
    __tablename__ = 'users'  # 表名称
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    xuehao = db.Column(db.String(50), nullable=False, unique=True, comment="学号")
    password = db.Column(db.String(20), nullable=False, comment="密码")
    email_id = db.Column(db.Integer, db.ForeignKey("emails.id"), nullable=False, comment="邮箱id来自数据表名：emails的id值")
    name = db.Column(db.String(200), nullable=False, default=None, comment="名字")
    clas = db.Column(db.String(200), nullable=False, default=None, comment="班级")
    gender = db.Column(db.String(200), nullable=False, default=None, comment="性别")
    qqh = db.Column(db.String(255), default=None, nullable=True, comment="QQ")
    room_num = db.Column(db.String(200), comment="宿舍号")
    dk_info = db.Column(db.Integer, nullable=False, default=0, comment="打卡信息是否为空")
    dk_time = db.Column(db.Time, nullable=False, default="07:00:00", comment="打卡时间")
    last_dk_time = db.Column(db.DateTime, nullable=False, default="2002-02-18 00:00:00", comment="上次打卡日期")
    state = db.Column(db.Integer, nullable=False, default=0, comment="账号状态：0启用  1禁用")
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.now, comment="添加时间")
    dk_num = db.Column(db.Integer, nullable=False, default=0, comment="打卡次数")
    check_state = db.Column(db.Boolean, nullable=False, default=0, comment="签到状态")
    check_time = db.Column(db.DateTime, nullable=False, default="2002-02-18 00:00:00", comment="签到时间")
    credit = db.Column(db.Integer, nullable=False, comment="积分")
    send_fail_num = db.Column(db.Integer, nullable=False, default=0, comment="用户拒收邮件次数")
    QjmQuota = db.Column(db.Integer, nullable=False, default=0, comment="额外请假名额")
    # 外键绑定
    # relationship('绑定的类型名', backref='articles':允许反向引用)
    email = db.relationship('Emails', backref='userslist')


# 网站配置
class Config(db.Model):
    __tablename__ = 'config'
    id = db.Column(db.Integer, primary_key=True)
    WebName = db.Column(db.String(255), nullable=False, comment="网站名称")
    WebUrl = db.Column(db.String(200), nullable=False, comment="前端地址")
    DKURL = db.Column(db.String(200), nullable=False, comment="学校打卡网站")
    Managers = db.Column(db.String(200), nullable=False, comment="管理员id/QQ")
    Groups = db.Column(db.String(200), nullable=False, comment="响应的QQ群")
    CorpID = db.Column(db.String(200), nullable=False, comment="企业微信ID")
    AccessToken = db.Column(db.Text(200), nullable=False, comment="企业微信token")
    AgentID = db.Column(db.String(200), nullable=False, comment="企业微信应用ID")
    CorpSecret = db.Column(db.String(200), nullable=False, comment="企业微信应用密钥")
    EmailGG = db.Column(db.Text(200), nullable=False, comment="邮件通知内容")
    AdminEmail = db.Column(db.String(200), nullable=False, comment="管理员的邮箱")
    SendEmailUserName = db.Column(db.String(200), nullable=False, comment="发送邮箱账号前缀")
    SendEmailUser = db.Column(db.String(200), nullable=False, comment="发送邮箱账号")
    SendEmailPassword = db.Column(db.String(200), nullable=False, comment="发送邮箱密码")
    SendEmailStmp = db.Column(db.String(200), nullable=False, comment="发送邮箱的服务器地址")
    SendEmailPort = db.Column(db.Integer, nullable=False, comment="发送邮箱的端口")
    SendEmailMaxNum = db.Column(db.Integer, nullable=False, comment="验证邮件的最大发送次数")
    SendFailMaxNum = db.Column(db.Integer, nullable=False, default=3, comment="邮件拒收的最大数量")
    gg = db.Column(db.String(200), nullable=False, unique=True, comment="公告")
    putdate = db.Column(db.DateTime, nullable=False, unique=True, default=datetime.now, comment="公告更新时间")
    QQGroupUrl = db.Column(db.String(200), nullable=False, comment="QQ群加群链接")
    KamiPayUrl = db.Column(db.String(200), nullable=False, comment="卡密购买地址")


# 积分配置
class CreditConfig(db.Model):
    __tablename__ = "credit_config"
    id = db.Column(db.Integer, primary_key=True)
    CheckCredit = db.Column(db.Integer, nullable=False, default=1, comment="签到获得积分数")
    QJMCredit = db.Column(db.Integer, nullable=False, default=3, comment="请假码积分单价")
    JoinCredit = db.Column(db.Integer, nullable=False, default=4, comment="新注册用户获得积分数")
    ActivityStartTime = db.Column(db.DateTime, nullable=False, comment="积分活动开始时间")
    ActivityEndTime = db.Column(db.DateTime, nullable=False, comment="积分活动结束时间")
    ActivityUserGetNum = db.Column(db.Integer, nullable=False, comment="普通群员获得最大积分数")
    ActivityAdminGetNum = db.Column(db.Integer, nullable=False, comment="群管理获得最大积分数")


# 黑名单
class Black(db.Model):
    __tablename__ = 'black'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    xuehao = db.Column(db.String(50), nullable=False, comment="学号")


# 邮箱验证码
class Emailcode(db.Model):
    __tablename__ = 'email_code'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False, comment="邮箱 unique:只存在一份")
    email_code = db.Column(db.Integer, nullable=False, comment="验证码")
    xuehao = db.Column(db.String(50), nullable=False, comment="学号")
    password = db.Column(db.String(200), nullable=False, comment="密码")
    name = db.Column(db.String(200), nullable=False, default=None, comment="名字")
    clas = db.Column(db.String(200), nullable=False, default=None, comment="班级")
    gender = db.Column(db.String(200), nullable=False, default=None, comment="性别")
    qqh = db.Column(db.String(255), default=None, nullable=True, comment="QQ")
    room_num = db.Column(db.String(200), comment="宿舍号")
    dk_info = db.Column(db.Integer, default=0, comment="打卡信息是否为空")
    dk_time = db.Column(db.Time, nullable=False, default="07:00:00", comment="打卡时间")
    verify_time = db.Column(db.Integer, default=1200, comment="验证超时时间，默认20分钟")
    time = db.Column(db.DateTime, nullable=False, default=datetime.now, comment="验证码发送时间,初次创建信息会自动获取当前时间")
    send_num = db.Column(db.Integer, default=0, comment="邮件发送次数")


# 未打卡残留用户
class NotDKUsers(db.Model):
    __tablename__ = "notdkusers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    xuehao = db.Column(db.String(50), nullable=False, unique=True, comment="学号")
    password = db.Column(db.String(20), nullable=False, comment="密码")
    email_id = db.Column(db.Integer, nullable=False, comment="emailid")
    state = db.Column(db.Integer, nullable=False, default=0, comment="账号状态：0启用  1禁用")


# 未添加打卡用户
class NADDUsers(db.Model):
    __tablename__ = "naddusers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    xuehao = db.Column(db.String(50), nullable=False, unique=True, comment="学号")
    password = db.Column(db.String(20), nullable=False, comment="密码")
    email = db.Column(db.String(200), nullable=False, comment="emailid")
    dk_time = db.Column(db.Time, nullable=False, default="07:00:00", comment="打卡时间")
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.now, comment="添加时间")


# 积分操作记录
class CreditLog(db.Model):
    __tablename__ = 'credit_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    xuehao = db.Column(db.String(50), nullable=False, unique=False, comment="学号")
    name = db.Column(db.String(200), nullable=False, comment="姓名")
    num = db.Column(db.Integer, nullable=False, comment="积分操作的数量")
    time = db.Column(db.DateTime, nullable=False, default=datetime.now, comment="操作积分的时间")
    bz = db.Column(db.String(200), nullable=False, comment="备注")
    # 排序-> 时间为主倒序
    __mapper_args__ = {
        "order_by": time.desc()  # -id
    }


# 积分活动表
class CreditActivit(db.Model):
    __tablename__ = "credit_activit"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    xuehao = db.Column(db.String(50), nullable=False, unique=True, comment="学号")
    name = db.Column(db.String(200), nullable=False, comment="姓名")
    num = db.Column(db.Integer, nullable=False, comment="送出积分数量")
    qqh = db.Column(db.String(200), nullable=False, comment="QQ号")
    time = db.Column(db.DateTime, nullable=False, default=datetime.now, comment="获得积分日期")


# 非学生账号
class NotStudentUser(db.Model):
    __tablename__ = "not_student_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, comment="账号")
    password = db.Column(db.String(200), nullable=False, comment="密码")
