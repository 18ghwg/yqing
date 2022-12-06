from config import logger
from exts import db, app
from module import UsersList
from module import hq_webinfo


# 更新用户信息
from module.mysql import Emails


def mod_qqh(_email):
    if '@qq.com' in _email:
        _qqh = _email.split('@')[0]
        try:
            _qqh = int(_qqh)
        except ValueError:
            _qqh = 1
        else:
            return _qqh
    else:
        return None


async def put_user_info():
    with app.app_context():
        _data = UsersList.query.filter_by().all()
        num = 0
        for user in _data:
            email = Emails.query.filter_by(id=user.email_id).first().email  # 邮箱
            # 获取信息
            info = hq_webinfo(user.xuehao, user.password)
            if isinstance(info, dict):
                name = info.get('name')
                clas = info.get('clas')
                gender = info.get('gender')
                qqh = info.get('qqh') if info.get('qqh') else mod_qqh(email)
                room_num = info.get('room_num')
                if room_num:
                    if "-" in room_num:
                        room_num = str(room_num).replace('-', '')
                    user.room_num = room_num
                # 更新信息
                user.clas = clas
                user.name = name
                user.gender = gender
                user.qqh = qqh
                db.session.commit()  # 提交数据
                num += 1
                logger.info(f"用户信息更新成功{num}宿舍号：{room_num}")
            else:
                pass
