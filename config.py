import ssl
from datetime import timedelta
from log import Logger

# logging
logger = Logger().logger

# 数据库的配置变量
HOSTNAME = '124.222.113.243'
PORT = '3306'
DATABASE = 'yqing_flask'
USERNAME = 'yqing_flask'
PASSWORD = 'wdGzDTamk6x7ETe6'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True
# session密钥
SECRET_KEY = "KJKLEREKRkeljrljeklsjrkflsFKL"
PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # 设置cookie为7天过期

# daka
fengexian = "\n------------\n"

# 全局取消证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# client
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "utf-8",
    "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36"
}

# 积分操作类别
credit_method = {
    "qjm_add": "新增请假码",
    "qjm_put": "更新请假码",
    "activit": "积分活动",
    "admin_add": "管理员充值",
    "admin_reduce": "管理员扣除",
    "user_check": "用户签到",
    "credit_move": "积分转移",
    "use_kami": "使用卡密"
}

# 请加额度操作类别
quota_method = {
    "use_kami": "使用卡密",
    "admin_add": "管理员充值",
    "admin_reduce": "管理员扣除",
    "qjm_add": "新增请假码",
    "quota_move": "额度转移",
}

# 卡密类型配置
kami_lib_config = {
    "Credit": "积分",
    "QjmQuota": "请假额度"
}
