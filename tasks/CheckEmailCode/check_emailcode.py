import asyncio
from datetime import datetime
from config import logger
from exts import app, db
from module import send_email
from module.mysql import Emailcode
from module.mysql.EmailClass import email_class


# 检测用户验证码是否验证
from module.mysql.WebClass import web_class


async def main():
    logger.info("【检测未验证】开始检测未验证邮件的用户")
    with app.app_context():
        _data = Emailcode.query.filter_by().all()  # 获取未验证邮箱列表
        _time = datetime.now()  # 获取当前时间
        for i in _data:
            # 更新信息
            i.time = _time  # 更新验证时间
            i.send_num += 1  # 增加发送次数
            # 获取信息
            _email = i.email  # 获取未验证邮箱
            _code = i.email_code  # 获取验证码
            _send_num = i.send_num  # 获取发送次数

            nr = '下午好！检测到您之前有在疫情自动打卡网站上添加账号!<br>' \
                 '由于你没有验证邮箱，导致你的账号一直处于未验证的状态；<br>你可以有以下选择：<br>' \
                 '<p><td align="justify"><table cellspacing="0" cellpadding="0" border="0" class="bmeButton" ' \
                 'align="left" style="border-collapse: separate;"><tbody><tr><td style="border-radius: 5px; ' \
                 'border-width: 0px; border-style: none; border-color: transparent; background-color: rgb(112, 97, ' \
                 '234); text-align: justify; font-family: Arial, Helvetica, sans-serif; font-size: 18px; padding: ' \
                 '10px 20px; font-weight: bold; word-break: break-word;" class="bmeButtonText"><span ' \
                 'style="font-family: Helvetica, Arial, sans-serif; font-size: 18px; color: rgb(255, 255, 255);">' \
                 '<a style="color: rgb(255, 255, 255); text-decoration: none;" target="_blank" draggable="false" ' \
                 f'href="{web_class.get_web_config()["WebUrl"]}/emailcode?email={_email}&code={_code}" data-link-type="web" ' \
                 'rel="noopener">重新验证</a></span></td></tr></tbody></table> ' \
                 '<td align="justify"><table cellspacing="0" cellpadding="0" border="0" class="bmeButton" ' \
                 'align="right" style="border-collapse: separate;"><tbody><tr><td style="border-radius: 5px; ' \
                 'border-width: 0px; border-style: none; border-color: transparent; background-color: rgb(112, 97, ' \
                 '234); text-align: justify; font-family: Arial, Helvetica, sans-serif; font-size: 18px; padding: ' \
                 '10px 20px; font-weight: bold; word-break: break-word;" class="bmeButtonText"><span ' \
                 'style="font-family: Helvetica, Arial, sans-serif; font-size: 18px; color: rgb(255, 255, 255);">' \
                 '<a style="color: rgb(255, 255, 255); text-decoration: none;" target="_blank" draggable="false" ' \
                 f'href="{web_class.get_web_config()["WebUrl"]}/emailcode/del?email={_email}" data-link-type="web" ' \
                 'rel="noopener">删除验证</a></span></td></tr></tbody></table></p> <br><br>'
            if _send_num <= email_class.get_sendemail_maxnum():  # 是否超过最大发送次数
                await send_email(_email, nr, '验证打卡账号')  # 发送提示邮件
                db.session.commit()  # 提交数据
            else:  # 用户一直不处理
                logger.info(f"【检测未验证】{_email}超过发送数量限制，不再发送并清理掉！")
                email_class.delemailcode(_email)  # 删除验证信息
                return False


# 检测未验证邮箱用户
def check_emailcode():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(main())
