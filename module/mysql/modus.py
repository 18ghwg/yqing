# -*- coding: utf-8 -*-
"""
@Time    : 2022/10/24 11:51
@Author  : ghwg
@File    : modus.py
通用的数据库操作方法
"""
import sqlalchemy

from exts import app, db


# 获取数据库配置
def get_sql_info(tablename: db.Model) -> dict:
    sql_data = tablename.query.get(1)
    if sql_data:
        # 表单字典数据
        info_list = {}
        # 获取表单数据
        sql_data = db.session.execute(f"select * from {sql_data.__tablename__}").first()
        keys = list(sql_data.keys())
        values = list(sql_data.values())
        for index, key in enumerate(keys):
            info_list[key] = values[index]
        return info_list
    else:
        return {}


# 修改数据库配置
def put_sql_info(tablename: db.Model, dic: dict) -> bool:
    """
    :param tablename: 数据表模型
    :param dic: 包含组名key和value的字典
    :return:
    """
    _data = tablename.query.filter_by(id=1)
    if _data:
        _data.update(dic)
        with app.app_context():
            db.session.commit()
        return True
    else:
        return False


# 处理数据库信息
def _mod(lis: sqlalchemy.engine.result.RowProxy) -> dict:
    """
    :param lis: 一组数据
    :return: 含有数据库所有信息的字典
    """
    keys = lis.keys()
    values = lis.values()
    _sql_data = {}  # 列表内的字典
    for index, key in enumerate(keys):
        _sql_data[key] = values[index]
    return _sql_data


# 获取数据库列表
def get_sql_list(tablename: db.Model, attribute: str, *order_by: str) -> list:
    """
    :param attribute: 列表属性
    :param tablename: 类名
    :param order_by: 正序留空或倒序DESC
    :return:
    """
    # 操作数据库

    _data = tablename.query.filter_by().all()
    if _data:
        # 获取表单数据
        sql_data = db.session.execute(
            f"select * from {_data[0].__tablename__} ORDER BY {attribute} {order_by[0] if order_by else ''}"
        ).fetchall()
        sql_list = [_mod(sql) for sql in sql_data]
        return sql_list
    else:
        return []


# 搜索数据库
def search_sql_info(tablename: db.Model, attribute: str, value: str):
    """
    :param tablename: 表名
    :param attribute: 搜索的键名
    :param value:  搜索的键值
    :return:
    """
    sql_data = tablename.query.filter_by().first()
    if sql_data:
        try:
            _data = db.session.execute(f"select * from {sql_data.__tablename__} WHERE {attribute}={value}").fetchall()
        except IndexError:
            return None
        else:
            return [_mod(sql) for sql in _data]
    else:
        return None

