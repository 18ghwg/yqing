import asyncio
from config import logger
from exts import app, db
from module import send_email
from module.emailcode import send_emailcode
from module.mysql import NADDUsers
from datetime import datetime

from module.mysql.WebClass import web_class


async def del_nadduser(xuehao: str):
    with app.app_context():
        # 在表中删除用户
        NADDUsers.query.filter_by(xuehao=xuehao).delete()  # 删除数据
        db.session.commit()  # 提交数据
        logger.info(f"【检测未提交】{xuehao}已从未提交表删除！")


async def main():
    start_time = datetime.now()
    hour = start_time.hour
    minute = start_time.minute
    time_now = f"{hour}:{minute}:00"
    with app.app_context():
        _data = NADDUsers.query.filter_by(dk_time=time_now).all()
        if _data:
            for i in _data:
                # 获取信息
                xuehao = i.xuehao
                password = i.password
                dk_time = i.dk_time
                join_date = i.join_date
                email = i.email
                await send_email(email,
                                 f"同学 检测到你{join_date}在疫情自动打卡网站上添加了你的账号"
                                 f"<br>现在对你的账号进行验证！<br>稍后发送验证结果！！", "账号添加提醒")
                send_data = send_emailcode(xuehao, password, email, dk_time, 10800)
                if send_data:  # 发送验证邮件
                    pass
                elif send_data is False:  # 账号或密码错误
                    nr = (str(xuehao) + f'<br>----------<br>你在{join_date}提交的疫情打卡账号或密码错误！<br>请重新提交！！<br>'
                          + '<td align="center"><table cellspacing="0" cellpadding="0" border="0" class="bmeButton" '
                            'align="center" style="border-collapse: separate;"><tbody><tr><td style="border-radius: 5px; '
                            'border-width: 0px; border-style: none; border-color: transparent; background-color: rgb(112, '
                            '97, 234); text-align: center; font-family: Arial, Helvetica, sans-serif; font-size: 18px; '
                            'padding: 15px 30px; font-weight: bold; word-break: break-word;" class="bmeButtonText"><span '
                            'style="font-family: Helvetica, Arial, sans-serif; font-size: 18px; color: rgb(255, 255, '
                            '255);"><a style="color: rgb(255, 255, 255); text-decoration: none;" target="_blank" '
                            f'draggable="false" href="{web_class.get_web_config()["WebUrl"]}" data-link-type="web" rel="noopener">重新提交  '
                            '</a></span></td></tr></tbody></table>')
                    await send_email(email, nr, f'密码校验失败')  # 发送密码错误提醒邮件
                else:
                    logger.info("【检测未提交】对未添加用户发送验证邮件时->邮件发送次数过多！")
                await del_nadduser(xuehao)  # 在表中删除用户
        else:
            # 当前时间没有未提交的用户！
            pass


# 检测未提交用户
def check_nadduser():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
