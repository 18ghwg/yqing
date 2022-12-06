# -*- coding: utf-8 -*-
"""
@Time    : 2022/11/12 9:50
@Author  : ghwg
@File    : home.py

"""

# 获取工作台消息数
import json
from datetime import timedelta, datetime
import requests
from module.mysql.QJMClass import qjm_class
from module.mysql.UserClass import user_class
from module.mysql.WebClass import web_class
from module.school.daka import check_user
from module.school.session import session


# 获取未读消息数
def get_home_msg_num(xuehao: str):
    check_data = check_user(xuehao, user_class.get_user_password(xuehao))
    if check_data is True:  # 密码正确
        try:
            url = f'{web_class.get_web_config()["DKURL"]}/student/content/admin/message/totalandunreadcount'
            res = session.get(url=url, timeout=2)
        except requests.Timeout:
            return [
                {
                    "TOTAL": 12,
                    "READ_IND": "1"
                }
            ]
        else:
            res = json.loads(res.text)
            return res
    else:  # 登陆失败
        return [
            {
                "TOTAL": 12,
                "READ_IND": "1"
            }
        ]


# 获取系统最后的消息
def get_home_mylastmsg(xuehao: str):
    check_data = check_user(xuehao, user_class.get_user_password(xuehao))
    if check_data is True:
        try:
            url = f'{web_class.get_web_config()["DKURL"]}/student/content/admin/message/mylastmessage'
            res = session.get(url)
        except requests.Timeout:
            return None
        else:
            # 获取请假信息
            qj_info = qjm_class.qjm_get_info(xuehao)
            if isinstance(qj_info, dict):
                qj_time = qj_info['time']  # 请假申请时间
                qj_jssj = qj_info['jssj']  # 请假结束时间
                if qj_time < datetime.now() < qj_jssj:  # 请假未结束
                    return {
                        "showTitle": "[提醒] 请假申请 (辅导员审核) 已通过，请知悉！",
                        "msgCreateTime": f"{datetime.now().month}-{datetime.now().day}",
                        "msgTitle": "[提醒] 请假申请 (辅导员审核) 已通过，请知悉！",
                        "msgContent": "返校后，次日需加做核酸。在系统里销假，上传材料。"
                    }
                else:  # 请假结束
                    return json.loads(res.text)
            else:  # 未获取到请假信息
                return None
    else:  # 账号校验失败
        return None


# 获取通知公告
def get_home_mylastnotice(xuehao: str):
    check_data = check_user(xuehao, user_class.get_user_password(xuehao))
    if check_data is True:
        try:
            url = f'{web_class.get_web_config()["DKURL"]}/student/content/admin/notices/mylastnotice'
            res = session.get(url)
        except requests.Timeout:
            return None
        else:
            return res.text
    else:
        return None


# 获取消息内容
def get_home_mymsg(xuehao: str):
    check_data = check_user(xuehao, user_class.get_user_password(xuehao))
    if check_data is True:
        # 在线获取信息
        try:
            url = f'{web_class.get_web_config()["DKURL"]}/student/content/tabledata/admin/message/mymessages?bSortable_0=false&bSortable_1=false&iSortingCols=1&iDisplayStart=0&iDisplayLength=10&iSortCol_0=3&sSortDir_0=desc&_t_s_=1668173791036'
            res = session.get(url=url, timeout=3)
        except requests.Timeout:
            return {"code": 400, "msg": "超时"}
        else:
            # 获取消息内容
            mymsg = json.loads(res.text)  # 转json
            # 处理请假通知
            qj_msg = {
                "MSG_TYPE": "1",
                "MENU_URL": None,
                "MSG_TITLE": "[提醒] 请假申请 (班主任审核) 已通过，请知悉！",
                "CDDM": "XSS0503",
                "MSG_URL": None,
                "DM": "16666683749891004416",
                "CREATE_TIME": "2022-10-25 11:26:14",
                "PARAMS": None,
                "DATA_M": "16666618162735932102",
                "WAP_MENU_URL": None,
                "MSG_CONTENT": ""
            }
            # 获取请假信息
            qj_info = qjm_class.qjm_get_info(xuehao)
            if isinstance(qj_info, dict):
                qj_time = qj_info['time']  # 请假申请时间
                qj_kssj = qj_info['kssj']  # 请假开始时间
                qj_jssj = qj_info['jssj']  # 请假结束时间
                if qj_time < datetime.now() < qj_jssj:  # 在请假中
                    if (qj_kssj - qj_time).seconds / 60 < 30:  # 请假申请的时间距离请假开始时间不超过半小时
                        qj_msg["CREATE_TIME"] = str(qj_kssj + timedelta(minutes=-33))  # 请假申请时间减半小时
                    else:
                        qj_msg["CREATE_TIME"] = str(qj_time)  # 默认就是请假申请时间
                    # 插入请假信息
                    mymsg["aaData"] = [qj_msg, *mymsg["aaData"]]
                else:  # 请假未开始或结束
                    pass
            else:  # 未获取到请假信息
                pass

            return mymsg
    else:
        return {"code": 400, "msg": "账号状态效验失败"}
