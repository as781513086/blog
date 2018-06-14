# -*- coding:utf-8 -*-
"""
@author:Zzb.
@file:config.py
@time:2018/6/111:34
"""
import os

debug = True

SECRET_KEY = os.urandom(24)

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'zxp121312'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'test1'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
