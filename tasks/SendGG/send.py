# -*- coding: UTF-8 -*-
#
# 需求：
import asyncio
import time
from config import logger
from exts import app
from module import send_email

# email
from module.mysql import Config, Emails

sleeptime = 3  # 暂停时间


async def get_gg():
    with app.app_context():
        _data = Config.query.filter_by().first()
    gg = _data.EmailGG  # 公告内容
    return gg


async def main():
    mailnum = 0
    try:
        gg = await get_gg()  # 获取邮件公告内容
        with app.app_context():
            email_list = Emails.query.filter_by().all()
            for i in email_list:
                mailnum += 1
                email = i.email
                # email = '2383262410@qq.com'
                await send_email(email, gg, f'疫情打卡公告{mailnum}')
                logger.info(f"【疫情打卡公告】\n{email}\n邮件发送成功！暂停{sleeptime}秒继续")
                time.sleep(sleeptime)  # 暂停
            logger.info("邮箱公告发送任务运行完成！")
            return True
    except Exception as e:
        logger.info(e)
        return False


def send():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())


if __name__ == '__main__':
    send()
