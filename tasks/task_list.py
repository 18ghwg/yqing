# flask 定时任务的方法
import hashlib


class Config(object):
    JOBS = [  # 任务列表
        {  # 任务1
            'id': '检测未验证邮箱',
            'func': 'tasks:check_emailcode',
            'trigger': 'cron',  # 定时方法
            'day': '*',  # 每天
            'hour': '13',  # 下午1点
            'minute': '30'  # 30分
        },
        # {  # 任务2
        #     'id': '疫情打卡now',
        #     'func': 'tasks:run',
        #     'trigger': 'cron',  # 定时方法
        #     'day': '*',  # 每天
        #     'hour': '*',  # 每分钟执行一次
        #     'minute': '*'
        # },
        {  # 任务3
            'id': '邮件公告',
            'func': 'tasks:send',
            'trigger': 'date',  # 定时方法
            'run_date': '2099-7-25 19:42:50'
        },
        {  # 任务4
            'id': '疫情打卡all',
            'func': 'tasks:run_all',
            'trigger': 'date',  # 定时方法
            'run_date': '2099-7-25 19:42:50'
        },
        {  # 任务5
            'id': '未提交检测',
            'func': 'tasks:check_nadduser',
            'trigger': 'cron',  # 定时方法
            'day': '*',  # 每天
            'hour': '*',  # 每分钟执行一次
            'minute': '*'
        },
        # {  # 任务6
        #     'id': '未打卡账号检测now',
        #     'func': 'tasks:check_ndk_user',
        #     'trigger': 'cron',  # 定时方法
        #     'day': '*',  # 每天
        #     'hour': '*',  # 每分钟执行一次
        #     'minute': '*'
        # },
        {  # 任务7
            'id': '未打卡账号检测all',
            'func': 'tasks:check_ndk_users',
            'trigger': 'date',  # 定时方法
            'run_date': '2099-7-25 19:42:50'
        },
        {  # 任务10
            'id': '清理积分日志',
            'func': 'tasks:clear',
            'trigger': 'cron',  # 定时方法
            'day': '7',
            'hour': '0',
            'minute': '0'  # 5分钟执行一次
        },
        {  # 任务12
            'id': '用户打卡时间检测修改',
            'func': 'tasks:check_user_dk_time',
            'trigger': 'cron',  # 定时方法
            'day': '*',  # 每天
            'hour': '*/1',  # 一小时执行一次
            'minute': '*'
        },
    ]

    SCHEDULER_API_ENABLED = True  # 开启API
    key = hashlib.md5(b'ghwg').hexdigest()
    _key = key[:5] + 'ghwg' + key[5:]
    SCHEDULER_API_PREFIX = f'/{_key}'  # api前缀
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 设置时区



