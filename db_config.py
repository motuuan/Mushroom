import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, static_folder='static', static_url_path='/static')
# python  pymysql  ORM:Flask_SQLAlchemy
# pip install pymysql
# pip install Flask_SQLAlchemy
#                                                        账号:密码@ip:port/数据库名
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/MushDB'
# 数据库初始化对象
db_init = SQLAlchemy(app)

