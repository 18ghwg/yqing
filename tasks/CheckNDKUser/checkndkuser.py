import asyncio
from datetime import datetime, timedelta
from config import logger
from exts import app
from module import sendwxbot
from module.mysql import UsersList, Emails
from tasks.YQDK import user_dk
from tasks.YQDK.module import up_ndkuser


async def check_now():
    now_time = datetime.now()  # 现在的时间
    today = datetime.strptime(now_time.strftime("%Y-%m-%d"), "%Y-%m-%d")  # 调用strftime方法就是对时间进行格式化
    dk_time = now_time - timedelta(minutes=20)
    dk_hour = dk_time.hour
    dk_minute = dk_time.minute
    dk_time = f"{dk_hour}:{dk_minute}"  # 获得20分钟前的时间
    logger.info(f"\n--------\n【检测未打卡】开始执行未打卡用户检测!\n【检测未打卡】当前检测的打卡时间：{dk_time}")
    # 获取用户列表
    with app.app_context():
        user_data = UsersList.query.filter_by(dk_time=dk_time).all()  # 20分钟前的打卡用户列表
        if user_data:  # 搜到结果了
            for user in user_data:
                xuehao = user.xuehao
                password = user.password
                email_id = user.email_id
                state = user.state
                last_dk_time = datetime.strptime(user.last_dk_time.strftime("%Y-%m-%d"), "%Y-%m-%d")  # 最后打卡时间
                # 检测打卡状态
                if last_dk_time < today:  # 用户今天未打卡->去打卡
                    if datetime.now().strftime("%H:%M:%S") >\
                            datetime.strptime(f"{now_time.strftime('%H:%M:%S')[:-2]}50", "%H:%M:%S").strftime("%H:%M:%S"):  # 打卡超时处理
                        logger.info(f"\n--------\n【检测未打卡】{xuehao}打卡超时处理：")
                        await up_ndkuser(xuehao, password, email_id, state)  # 添加到未打卡账号表中
                    else:
                        logger.info(f'【检测未打卡】{(await user_dk(xuehao))["msg"]}')  # 执行打卡
                elif last_dk_time == today:  # 今日已打卡
                    # print(f"检测到{xuehao}今日已打卡")
                    pass
                else:
                    logger.info(f"【检测未打卡】获取到的当前日期大于{xuehao}最后打卡日期，检查服务器时间是否正确")
        else:
            logger.info(f"【检测未打卡】未搜到当前时间{dk_time}的未打卡用户")


# 检测所有用户打卡状态
async def check_all():
    ndk_user_num = 0  # 未打卡用户数量
    dk_user_num = 0  # 已打卡用户
    now_time = datetime.now()  # 现在的时间
    today = datetime.strptime(now_time.strftime("%Y-%m-%d"), "%Y-%m-%d")  # 调用strftime方法就是对时间进行格式化
    with app.app_context():
        user_list = UsersList.query.filter_by().all()
    for user in user_list:
        last_dk_time = datetime.strptime(user.last_dk_time.strftime("%Y-%m-%d"), "%Y-%m-%d")  # 最后打卡时间
        if last_dk_time < today:  # 未打卡
            ndk_user_num += 1  # 未打卡数量加一
        elif last_dk_time == today:  # 今日已打卡
            dk_user_num += 1  # 已打卡用户加一
        else:  # 服务器时间不对
            logger.info("【检测未打卡】用户打卡时间大于今天的日期，请查看服务器时间是否正确！")
    sendwxbot("`未打卡账号检测`运行完成\n"
              "**信息：**\n"
              f">未打卡用户数量：<font color=\"info\">{ndk_user_num}</font>\n"
              f">打卡用户数量：<font color=\"warning\">{dk_user_num}</font>\n"
              f">总用户数量：<font color=\"info\">{len(user_list)}</font>\n"
              f">**提示：未打卡用户可能是自己打卡了！**")
    return {"ndk_user_num": ndk_user_num, "dk_user_num": dk_user_num, "user_num": len(user_list)}


# 检测当前时间未打卡用户
def check_ndk_user():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(check_now())


# 检测所有用户打卡状态
def check_ndk_users():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    logger.info(loop.run_until_complete(check_all()))
