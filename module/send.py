# coding=utf-8
import random
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

import httpx
import requests

from config import logger
from module.mysql.NoticeClass import notice_class
from module.mysql.WebClass import web_class


async def send_email(useremail, nr, subject):
    """
    :param useremail: 收件用户邮箱
    :param nr: 邮件内容
    :param subject: 邮件主题
    :return:
    说明：发送失败是因为编码问题，你的电脑是中文名称，请在服务器上测试邮件功能
    """
    email_data = web_class.get_web_config()  # 获取邮箱配置
    try:
        my_sender = str(email_data["SendEmailUser"])  # 发件人邮箱账号
        my_pass = str(email_data["SendEmailPassword"])  # 发件人邮箱密码
        stmpurl = str(email_data["SendEmailStmp"])  # stmp服务器地址
        stmp_port = int(email_data["SendEmailPort"])  # 邮箱服务器端口
        msg = MIMEText(
            '<div style="background-color:white;border-top:2px solid #12ADDB;box-shadow:0 1px 3px #AAAAAA;line-height:180%;padding:0 15px 12px;width:500px;margin:50px auto;color:#555555;font-family:"Century Gothic","Trebuchet MS","Hiragino Sans GB",微软雅黑,"Microsoft Yahei",Tahoma,Helvetica,Arial,"SimSun",sans-serif;font-size:12px;">          <h2 style="border-bottom:1px solid #DDD;font-size:14px;font-weight:normal;padding:13px 0 10px 8px;"><span style="color: #12ADDB;font-weight: bold;">&gt; </span>系统消息</h2>          <div style="padding:0 12px 0 12px;margin-top:18px">    <p>' + nr + f'</p><p>本邮件为自动发送，如有疑问，联系我<a style="text-decoration:none; color:#12addb"  href="mailto:2383262410@qq.com" target="_blank">观后无感</a>，欢迎再次光临 <a style="text-decoration:none; color:#12addb" href="{web_class.get_web_config()["WebUrl"]}" target="_blank">南科疫情自动打卡</a>，用户后台 <a style="text-decoration:none; color:#12addb" href="{web_class.get_web_config()["WebUrl"]}/user/login" target="_blank">登录</a>。</p>          </div>      </div>',
            'html', 'utf-8')
        msg['From'] = formataddr(["疫情自动打卡", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["同学", useremail])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = f"{subject}"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL(stmpurl, stmp_port)  # 发件人邮箱中的SMTP服务器、端口
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [useremail, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        logger.info("邮件发送成功！")
        return True
    except:
        logger.info("邮件发送失败！")
        return False


# 企业应用推送
# 获取token
def get_token():
    token = notice_class.get_access_token()
    # token检测
    check_res = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/get_api_domain_ip?access_token={token}").json()
    if check_res["errcode"] == 40014 or check_res["errcode"] == 42001:  # access_token失效
        logger.info("access_token已失效，正在重新获取...")
        _res = requests.get(
            f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={web_class.get_web_config()['CorpID']}"
            f"&corpsecret={web_class.get_web_config()['CorpSecret']}").json()
        try:
            token = _res["access_token"]
            notice_class.put_access_token(token)
            return token
        except Exception as e:
            logger.info(f"获取token失败，原因：{e}")
            return None
    else:  # access_token有效
        logger.info("access_token有效")
        return token


# 发送企业应用
def sendwxbot(nr):
    token = get_token()
    if token is None:
        return
    else:
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"
        msg = {
            "touser": "@all",
            "msgtype": "markdown",
            "agentid": web_class.get_web_config()["AgentID"],
            "markdown": {"content": nr},
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        res = requests.post(url=url, json=msg).json()
        if res['errcode'] == 0:
            logger.info("微信应用通知发送成功！")
        else:
            logger.info(f"微信应用通知发送失败！内容：{res}")
