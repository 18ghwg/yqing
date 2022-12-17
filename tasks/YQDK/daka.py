import asyncio
from datetime import datetime, date
import hashlib
import json
import re
import time
from typing import Union

import cv2
import httpx
from exts import app
from config import fengexian, logger, headers
from module.mysql import UsersList, Emails
from module.mysql.WebClass import web_class
from .module import modstate, deluser, dk_nums, up_ndkuser, get_ndkusers, del_ndkuser, set_dk_info_state, get_user_info, \
    yzm
from module import send_email, sendwxbot

usernum = 0  # 账号数量
cg_user = 0  # 打卡成功数量
sb_user = 0  # 打卡失败数量
mz = ''  # 名字
xgym_dm = {
    '0': '未接种',
    '1': '已接种未完成',
    '2': '已接种已完成',
    '3': '已接种加强针',
    '4': '未接种加强针',
}


# 密码加密
def jiami(passwd: str) -> str:
    temp = hashlib.md5()
    temp.update(str(passwd).encode())
    temp = temp.hexdigest()
    return temp[:5] + 'a' + temp[5:9] + 'b' + temp[9:-2]


# 登录获取Cookie
async def login(xuehao: str, mima: str, email: str, client_set) -> bool:
    """
    :param email: 邮箱
    :param xuehao: 学号
    :param mima: 密码
    :param client_set: client线程
    :return: True：登陆成功  False：登录超时
    """
    global mz
    # logger.info(res_one)
    data = {
        'uname': xuehao,
        'pd_mm': jiami(mima)
    }
    try:
        await yzm(client_set)  # 过验证码
        await client_set.get(url=web_class.get_web_config()["DKURL"])  # 访问网站首页
        res = await client_set.post(web_class.get_web_config()["DKURL"] + '/student/website/login', data=data)
        login_data = json.loads(res.text)
    except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.ConnectError):
        return False
    except json.decoder.JSONDecodeError:
        sendwxbot("疫情打卡：服务器ip被封，用户登录失败")
        return False
    else:
        if "goto2" in str(login_data):  # 登陆成功
            mz = (await get_user_info(xuehao))["xhxm"]  # 获取名字
            return True
        else:
            login_failmesg = login_data['msg']
            logger.error(f"{xuehao}\n登陆失败！原因：{login_failmesg}")
            await modstate(xuehao, 'disabled')  # 禁用失效账号
            nr = (
                    f'{str(xuehao)}<br>----------<br>{login_failmesg}<br>'
                    + '<td align="center"><table cellspacing="0" cellpadding="0" border="0" class="bmeButton" '
                      'align="center" style="border-collapse: separate;"><tbody><tr><td style="border-radius: 5px; '
                      'border-width: 0px; border-style: none; border-color: transparent; background-color: rgb(112, '
                      '97, 234); text-align: center; font-family: Arial, Helvetica, sans-serif; font-size: 18px; '
                      'padding: 15px 30px; font-weight: bold; word-break: break-word;" class="bmeButtonText"><span '
                      'style="font-family: Helvetica, Arial, sans-serif; font-size: 18px; color: rgb(255, 255, '
                      '255);"><a style="color: rgb(255, 255, 255); text-decoration: none;" target="_blank" '
                      f'draggable="false" href="{web_class.get_web_config()["WebUrl"]}" data-link-type="web" rel="noopener">重新提交  '
                      '</a></span></td></tr></tbody></table>')
            await send_email(email, nr, f'疫情打卡出错')  # 发送密码错误提醒邮件


# 获取DM
async def get_dm(client_set) -> Union[str, bool]:
    res = await client_set.get(
        url=f'{web_class.get_web_config()["DKURL"]}/student/content/student/temp/zzdk/lastone')

    try:
        DM = json.loads(res.text)["dm"]
        return DM
    except KeyError:
        return False


# 获取打卡token
async def get_token(client_set: httpx.AsyncClient) -> Union[str, bool]:
    res = await client_set.get(
        url=web_class.get_web_config()["DKURL"] + f'/student/wap/menu/student/temp/zzdk/_child_/edit')
    # print(res.text)
    try:
        zzdk_token = re.findall('<input class="hidden" type="text" id="zzdk_token" name="zzdk_token" value="(.+?)"/>',
                                res.text)[0]  # 正则提取token
        logger.info(f"获取到Token:{zzdk_token}")
        return zzdk_token
    except Exception as e:
        logger.error(f"获取Token失败！原因：{e}")
        return False


# 获取历史信息
async def get_last_info(client_set) -> Union[dict, None]:
    global sb_user
    try:
        res = await client_set.get(
            "https://xgyyx.njpi.edu.cn/student/content/tabledata/student/temp/zzdk?bSortable_0=false&bSortable_1=true&iSortingCols=1&iDisplayStart=0&iDisplayLength=1&iSortCol_0=1&sSortDir_0=desc"
            )
        DMID = res.json()["aaData"][0]["DM"]
        dk_info = await client_set.get(f"https://xgyyx.njpi.edu.cn/student/content/student/temp/zzdk/{DMID}"
                                       )
        return dk_info.json()
    except:
        return None


# 检查今日是否打卡
async def check_dked(client_set) -> bool:
    """
    :return: 已打卡：True , 未打卡：False
    """
    today = date.today()
    res = await client_set.get(
        url=f'{web_class.get_web_config()["DKURL"]}/student/content/tabledata/student/temp/zzdk?bSortable_0=false&bSortable_1=true&iSortingCols=1&iDisplayStart=0&iDisplayLength=1&iSortCol_0=1&sSortDir_0=desc'
    )
    if str(today) == json.loads(res.text)['aaData'][0]['DKRQ']:
        return True
    else:
        return False


# 获取经纬度坐标
async def get_location(address: str):
    new_client = httpx.AsyncClient()
    new_client.headers = headers
    resp = await new_client.get(
        "https://api.map.baidu.com/geocoder",
        params={"address": address, "output": "json"}
    )
    try:
        _data = json.loads(resp.text)["result"]["location"]
        lng = _data['lng']
        lat = _data['lat']
        return f'{lng}, {lat}'
    except Exception as e:
        logger.error(f"打卡坐标获取失败{e}")
        return False
    finally:
        await new_client.aclose()


# 处理None信息
async def this_none(_none: str) -> str:
    if _none is None:
        _none = ""
    else:
        _none = _none
    return _none


async def set_jkm1_xcm1(abled):
    if abled == 1:
        return "绿色"
    elif abled == 2:
        return "黄色"
    elif abled == 3:
        return "红色"
    else:
        return "绿色"


async def set_hsjc(abled):
    if abled == 1:
        return "是"
    elif abled == 0:
        return "否"


# 打卡
async def daka(xuehao: str, email: str, client_set) -> Union[str, bool]:
    global cg_user
    last_lnfo = await get_last_info(client_set)
    if isinstance(last_lnfo, dict):
        await set_dk_info_state(xuehao, 1)  # 设置打卡信息状态：1
        # 备注处理
        if last_lnfo['bz'] is None and last_lnfo['sfzx'] == '0':
            bz = "放假了"
        else:
            bz = await this_none(last_lnfo['bz'])
        #
        if last_lnfo['xgym'] is None:
            xgym = "0"
        else:
            xgym = last_lnfo['xgym']
        if last_lnfo['hsjc']:
            hsjc = last_lnfo['hsjc']
            hsjc1 = await set_hsjc(hsjc)
        else:
            hsjc = 1
            hsjc1 = "是"
        data = {
            'dkdz': last_lnfo['dkd'] + (last_lnfo['jzdXian']['mc'] if last_lnfo['jzdXian'] else ''),
            'dkdzZb': await get_location(last_lnfo['dkd']),
            'dkly': 'baidu',
            'dkd': last_lnfo['dkd'],
            'zzdk_token': await get_token(client_set),
            'jzdValue': f'{"320000" if last_lnfo["jzdSheng"] is None else last_lnfo["jzdSheng"]["dm"]},{"320100" if last_lnfo["jzdShi"] is None else last_lnfo["jzdShi"]["dm"]},{"" if last_lnfo["jzdXian"] is None else last_lnfo["jzdXian"]["dm"]}',
            'jzdSheng.dm': "320000" if last_lnfo['jzdSheng'] is None else last_lnfo['jzdSheng']['dm'],
            'jzdShi.dm': "320100" if last_lnfo['jzdShi'] is None else last_lnfo['jzdShi']['dm'],
            'jzdXian.dm': "" if last_lnfo['jzdXian'] is None else last_lnfo['jzdXian']['dm'],
            'jzdDz': last_lnfo['jzdDz'],
            'jzdDz2': last_lnfo['jzdDz2'],
            'lxdh': last_lnfo['lxdh'],
            'sfzx': last_lnfo['sfzx'],
            'sfzx1': '不在校' if last_lnfo['sfzx'] != "1" else "在校",
            'twM.dm': last_lnfo['twM']['dm'],
            'tw1': last_lnfo['twM']['mc'],
            'tw1M.dm': "",
            'tw11': "",
            'tw2M.dm': "",
            'tw12': "",
            'tw3M.dm': "",
            'tw13': "",
            'yczk.dm': last_lnfo['yczk']['dm'],
            'yczk1': last_lnfo['yczk']['mc'],
            'fbrq': await this_none(last_lnfo['fbrq']),
            'jzInd': await this_none(last_lnfo['jzInd']),
            'jzYy': await this_none(last_lnfo['jzYy']),
            'zdjg': await this_none(last_lnfo['zdjg']),
            'fxrq': await this_none(last_lnfo['fxrq']),
            'brStzk.dm': last_lnfo['brStzk']['dm'],
            'brStzk1': last_lnfo['brStzk']['mc'],
            'brJccry.dm': last_lnfo['brJccry']['dm'],
            'brJccry1': last_lnfo['brJccry']['mc'],
            'jrStzk.dm': last_lnfo['jrStzk']['dm'],
            'jrStzk1': last_lnfo['jrStzk']['mc'],
            'jrJccry.dm': last_lnfo['jrJccry']['dm'],
            'jrJccry1': last_lnfo['jrJccry']['mc'],
            'jkm': 1 if last_lnfo['jkm'] is None else last_lnfo['jkm'],
            'jkm1': await set_jkm1_xcm1(last_lnfo['jkm']),
            'xcm': 1 if last_lnfo['xcm'] is None else last_lnfo['xcm'],
            'xcm1': await set_jkm1_xcm1(last_lnfo['xcm']),
            'xgym': xgym,
            'xgym1': xgym_dm[xgym],
            'hsjc': hsjc,
            'hsjc1': hsjc1,
            'bz': bz,
            'operationType': 'Create',
            'dm': ''}
    else:  # 历史打卡信息获取为空
        await set_dk_info_state(xuehao, 0)  # 设置打卡信息状态为空：0
        return False
    # logger.info(data)
    res = await client_set.post(web_class.get_web_config()["DKURL"] + '/student/content/student/temp/zzdk', data=data)
    logger.info(res.text)
    dk_state = json.loads(res.text)['result']  # 打卡状态：bool
    if dk_state:
        cg_user += 1  # 打卡成功加一
        dknumdata = await dk_nums(xuehao)  # 记录打卡次数至数据库
        logger.info(f"{mz}今日打卡成功！\n邮箱：{email}\n打卡地址：{last_lnfo.get('dkd')}")
        return f"{mz}<br>------------<br>今日疫情打卡成功！<br>{dknumdata}<br>邮箱：{email}<br>打卡地址：{last_lnfo.get('dkd')}"  # 邮件内容
    else:
        tishi = json.loads(res.text)['errorInfoList'][0]['message']  # 打卡提示信息
        if "非法" in tishi:
            return False
        else:
            return f'学号：{xuehao}<br>{tishi}'


async def check_url():  # 等待学校服务器开机
    new_client = httpx.AsyncClient()  # 创建新的client
    new_client.headers = headers
    try:
        res = await new_client.get(url=web_class.get_web_config()["DKURL"])
        logger.info("检测到服务器开机！-> 继续执行任务！")
        await new_client.aclose()  # 关闭链接
        return True
    except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.ConnectError):
        time.sleep(10)
        await check_url()


async def main():
    global usernum, sb_user, cg_user
    mailnum = 0  # 邮件发送次数
    usernum = 0  # 账号数量
    cg_user = 0  # 打卡成功数量
    sb_user = 0  # 打卡失败数量
    start_time = datetime.now()
    # client
    client = httpx.AsyncClient()
    client.headers = headers
    client.timeout = httpx.Timeout(4.0)
    with app.app_context():
        user_list = UsersList.query.filter_by().all()  # 用户列表
    for i in user_list:
        mailnum += 1
        email_id = i.email_id
        with app.app_context():
            email_data = Emails.query.filter_by(id=email_id).first()
        email = email_data.email
        # 信息
        xuehao = i.xuehao
        password = i.password
        state = i.state
        logger.info("参数获取成功：")
        logger.info("账号：" + str(xuehao))
        usernum += 1  # 账号数量+1
        if state == 0:  # 有效
            login_data = await login(xuehao, password, email, client)
            if login_data:
                if not await check_dked(client):  # 今日未打卡
                    dk_data = await daka(xuehao, email, client)
                    if isinstance(dk_data, str):  # 如果dk_data是str类型
                        await send_email(email, dk_data, f'疫情打卡成功{xuehao}-{mailnum}')  # 打卡成功邮件
                else:
                    logger.info(f"邮箱：{email}\n{mz}今日已有打卡记录！")
                    sb_user += 1

            elif login_data is False:
                logger.info(f"{xuehao}登陆失败：服务器连接超时!\n等待服务器响应...")
                if await check_url():
                    await daka(xuehao, email, client)
        else:
            logger.info("检测到无效账号，即将处理掉！")
            await deluser(xuehao)  # 删除失效账号
        logger.info(fengexian)
    await client.aclose()
    end_time = datetime.now()
    sendwxbot(
        "`疫情打卡任务运行完成`\n"
        f">账号数量：<font color=\"info\">{usernum}</font>\n"
        f"打卡成功：<font color=\"warning\">{cg_user}</font>\n"
        f"打卡失败(含重复打卡)：<font color=\"info\">{sb_user}</font>\n"
        f"用时：<font color=\"warning\">{str(end_time - start_time).split('.')[0]}</font>")  # 发送微信提醒
    logger.info(f"执行完成{fengexian}账号数量：{usernum}\n打卡成功：{cg_user}\n打卡失败(含重复打卡)：{sb_user}")


# 根据用户设置的打卡时间
async def dk_now():
    # client
    client = httpx.AsyncClient()
    client.headers = headers
    client.timeout = httpx.Timeout(4.0)
    mailnum = 0
    start_time = datetime.now()
    hour = start_time.hour
    minute = start_time.minute
    time_now = f"{hour}:{minute}:00"
    logger.info(f"【疫情打卡】当前打卡时间：{time_now}")
    with app.app_context():
        user_list = UsersList.query.filter_by(dk_time=time_now).all()  # 当前打卡时间的用户列表
        ndkuser_list = await get_ndkusers()  # 未打卡用户列表
        user_lists = user_list + ndkuser_list  # 当前时间用户和未打卡用户汇总
    if user_lists:
        for i in user_lists:
            mailnum += 1
            with app.app_context():
                email_data = Emails.query.filter_by(id=i.email_id).first()
                if email_data:  # 获取到信息
                    pass
                else:  # 没有搜到信息
                    logger.info(f"【疫情打卡】未找到该账号[{i.xuehao}]的邮箱信息")
                    await del_ndkuser(i.xuehao)
                    continue  # 退出本次循环

            # 获取信息
            email = email_data.email
            xuehao = i.xuehao
            password = str(i.password)
            state = int(i.state)
            logger.info("【疫情打卡】参数获取成功：")
            logger.info("【疫情打卡】账号：" + str(xuehao))
            if datetime.now().strftime("%H:%M:%S") > \
                    datetime.strptime(f"{start_time.strftime('%H:%M:%S')[:-2]}45",
                                      "%H:%M:%S").strftime("%H:%M:%S"):  # 如果打卡时用户过多即将超时,留15秒添加用户到未打卡表中
                await up_ndkuser(xuehao, password, i.email_id, state)  # 添加到未打卡账号表中
                continue  # 退出此次for循环
            else:  # 没有超时
                if state == 0:  # 有效
                    if await login(xuehao, password, email, client):
                        if not await check_dked(client):  # 今日未打卡
                            dk_data = await daka(xuehao, email, client)
                            if isinstance(dk_data, str):  # 如果dk_data是str类型
                                await send_email(email, dk_data, f'疫情打卡成功{xuehao}-{mailnum}')  # 打卡成功邮件
                            else:  # 历史打卡信息为空
                                logger.info(f"【疫情打卡】{xuehao}打卡失败：获取打卡信息失败->没有一条历史打卡记录；发送提醒邮件：")
                                await send_email(email, f'{xuehao}打卡失败：获取打卡信息失败->没有一条历史打卡记录<br>'
                                                        f'请先去学校网站手动打卡一次，本程序才能获取历史打卡信息！',
                                                 f'疫情打卡失败{mailnum}')  # 打卡成功邮件
                        else:
                            logger.info(f"【疫情打卡】邮箱：{email}\n{mz}今日已有打卡记录！")
                    else:
                        logger.info(f"【疫情打卡】{xuehao}登陆失败：服务器连接超时!\n等待服务器响应...")
                        if await check_url():
                            await client.aclose()  # 关闭现有连接，避免多线
                            await daka(xuehao, email, client)
                else:
                    logger.info("【疫情打卡】检测到无效账号，即将处理掉！")
                    await deluser(xuehao)  # 删除失效账号
                logger.info(fengexian)
                await del_ndkuser(xuehao)  # 删除未打卡用户
        await client.aclose()  # 关闭client连接
        end_time = datetime.now()
        logger.info(f"【疫情打卡】执行完成{fengexian}耗时：{end_time - start_time}")
    else:
        # 这个时间段没有账号打卡！
        logger.info(f"【疫情打卡】这个时间：{time_now}没有用户需要打卡！")
        pass


# 单个用户打卡方法
# 用于在视图函数中调用
async def user_dk(xuehao: str):
    client_dk = httpx.AsyncClient()
    client_dk.headers = headers
    _data = UsersList.query.filter_by(xuehao=xuehao).first()
    if _data:  # 在用户表中
        _email = (Emails.query.filter_by(id=_data.email_id).first()).email  # 邮箱
        _state = _data.state  # 用户状态
        _password = _data.password  # 获取密码
        _name = _data.name  # 姓名
        logger.info(f"{fengexian}获取到信息：[{xuehao}]{_name}")
        if _state == 0:  # 有效
            if await login(xuehao, _password, _email, client_dk):  # 登陆成功
                if not await check_dked(client_dk):  # 今日未打卡
                    _dk_data = await daka(xuehao, _email, client_dk)
                    if _dk_data:
                        await send_email(_email, _dk_data, "疫情打卡通知")
                        info = {"code": 200, "msg": f"{_name}今日打卡成功！"}
                    else:  # 获取信息失败
                        info = {"code": 400, "msg": "获取打卡信息失败<br>请重新打卡！"}
                else:  # 已打卡
                    info = {"code": 400, "msg": f"打卡失败：{_name}今日有打卡记录！"}
            else:  # 超时
                info = {"code": 400, "msg": "打卡失败：学校服务器关机了，白天再来！"}
        else:  # 用户无效
            info = {"code": 400, "msg": f"{_name}用户状态无效，不能提供打卡！"}
            await deluser(xuehao)  # 删除失效账号
    else:  # 用户没在表中
        info = {"code": 400, "msg": "无效的用户！"}
    await client_dk.aclose()  # 关闭链接
    return info


# 根据用户设置打卡时间打卡
def run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(dk_now())


# 全部用户执行打卡
def run_all():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())


# 用户后台打卡
def user_daka(xuehao):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(user_dk(xuehao))
