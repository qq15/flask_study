#!/usr/bin/env python3
from flask import Flask
from flask import render_template
from flask import request
from random import randint
import pymysql
import hashlib

app = Flask(__name__)


def md5_calc(_str, salt = None):
    if not salt:
        salt = randint(10000, 9999999)
        m = hashlib.md5(str(salt).encode('utf-8'))
        m.update(_str.encode('utf-8'))
        return m.hexdigest(), salt
    else:
        m = hashlib.md5(str(salt).encode('utf-8'))
        m.update(_str.encode('utf-8'))
        return m.hexdigest()


@app.route('/test')
def test():
    return u'A test'


@app.route('/')
def index():
    return u'Hello World!'


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('reg.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        cursor.execute("SELECT * FROM user1 WHERE username='{}'; ".format(username))
        if cursor.fetchall():
            return '该帐号已被注册'
        else:
            password, salt = md5_calc(password)
            cursor.execute("INSERT INTO user1(username, password, salt) VALUES('{}','{}', '{}');".format(username, password, salt))
            conn.commit()
            return '你已经注册成功'


@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'GET':
        return render_template('log.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        cursor.execute("SELECT * FROM user1 WHERE username='{}';".format(username))
        try:
            salt = cursor.fetchall()[0][3]
            password = md5_calc(password, salt)
            cursor.execute("SELECT * FROM user1 WHERE username='{}' and password='{}' ; ".format(username, password))
            '''
            try:
                cursor.fetchall()
                return '登录成功,新的ip是104.223.78.40，其它不变'
            except:
                return '帐号或密码错误'
            '''
            if cursor.fetchall():
                return '登录成功,新的ip是104.223.78.40,其它不变'
            else:
                return '帐号或密码错误'
        except:
            return '帐号或密码错误'


if __name__ == '__main__':
    conn = pymysql.connect(
        host='localhost',
        port='0.0.0.0',
        user='root',
        passwd='a',
        db='test1'
    )
    cursor = conn.cursor()
    app.run(port=4000, host="0.0.0.0")
