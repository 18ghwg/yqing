# 数据库操作
from datetime import datetime
from config import logger
from exts import db, app
from module.mysql import Config


# 公告类
class NoticeClass:
    # 更新web公告
    @classmethod
    def putggs(cls, content: str) -> bool:
        """
        :param content: 内容
        :return: True：更新成功  False：更新失败
        """
        putdata = Config.query.get(1)
        putdata.gg = content
        putdata.putdate = datetime.now()  # 更新时间
        db.session.commit()  # 提交数据
        ggdata = Config.query.get(1).gg  # 当前公告内容
        if ggdata == content:
            return True
        else:
            return False

    # 获取access_token
    @classmethod
    def get_access_token(cls):
        with app.app_context():
            get_token_data = Config.query.get(1)
            return get_token_data.AccessToken

    # 更新access_token
    @classmethod
    def put_access_token(cls, token: str):
        with app.app_context():
            put_data = Config.query.get(1)
            put_data.AccessToken = token
            db.session.commit()  # 提交更新
            logger.info("access token已更新！")


notice_class = NoticeClass()  # 实例化对象
