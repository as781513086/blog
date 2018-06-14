# -*- coding:utf-8 -*-
"""
@author:Zzb.
@file:manage.py
@time:2018/6/1113:04
"""

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from run import app
from exts import db
from models import User, Question, Answer

#用来实现命令行操作
manager = Manager(app)
#绑定app，db
migrate  = Migrate(app,db)
#把迁移命令添加到manager中
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()