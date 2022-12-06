# -*- coding: utf-8 -*-
"""
@Time    : 2022/11/6 22:06
@Author  : ghwg
@File    : ClearLogs.py

"""
from datetime import datetime, timedelta
from sqlalchemy import func
from config import logger
from exts import app, db
from module.mysql import CreditLog


# 清除log数据库
def clear():
    wq_days = 7  # 保留日志的天数
    date_now = datetime.now().date()  # 当前日期
    with app.app_context():
        log_data = CreditLog.query.filter(func.DATE(CreditLog.time) < date_now - timedelta(days=wq_days)).all()
        CreditLog.query.filter(func.DATE(CreditLog.time) < date_now - timedelta(days=wq_days)).delete(False)
        db.session.commit()  # 提交删除
        logger.info(f"本次清理日志{len(log_data)}条")
