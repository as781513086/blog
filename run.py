# -*- coding:utf-8 -*-
"""
@author:Zzb.
@file:__init__.py
@time:2018/6/111:35
"""

from flask import Flask,render_template,Request,request, redirect, url_for, session
import config
import  os
from flask import Flask
from exts import db
from models import User,Question, Answer
from functools import wraps

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

#登录限制
def login_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

@app.route('/')
@login_limit
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,User.password == password).first()
        if user:
            session['user_id'] = user.id
            #保存cooike
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return '手机号码或密码错误！'


@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        #判断
        if telephone == '' or username == '' or password == '':
            print(telephone,username,password)
            return '选项不能为空!'
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '该手机号码已被注册！'
        else:
            if password != password2:
                return '两次密码不相等，请重试！'
            else:
                user = User(telephone = telephone, username = username,password = password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_limit
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')

        question = Question(title = title , content = content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question = question_model)

@app.route('/add_answer/', methods=['POST'])
@login_limit
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content = content)
    answer_id = session['user_id']
    user = User.query.filter(User.id == answer_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail' , question_id = question_id))

@app.context_processor
def my_context():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run()
