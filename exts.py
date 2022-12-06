from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter

app = Flask(__name__, static_url_path='')


# 限流器全局配置
def limit_key_func():
    return str(request.headers.get("X-Forwarded-For", '127.0.0.1'))


limiter = Limiter(
    app, key_func=limit_key_func,
    default_limits=["20 per minute"],
    storage_uri="redis://default:sun0218..@127.0.0.1:6379",
)
db = SQLAlchemy(session_options={"expire_on_commit": False})
