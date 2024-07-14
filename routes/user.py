from flask import Blueprint, request, redirect, url_for, session, render_template, flash
import json
from services.user import User_operation

user = Blueprint('user', __name__)

@user.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        email = data['email']
        gender = data['gender']
        password = data['password']
        confirmpassword = data['confirmpassword']

        if password != confirmpassword:
            message = '确认密码与密码不一致，请重新输入!'
            return redirect(url_for('user.register', message=message))

        u = User_operation()
        result = u.register(username, email, gender, password)

        if result.json['code'] == 0:
            message = result.json['message']
            return redirect(url_for('user.login', message=message))
        else:
            message = result.json['message']
            return redirect(url_for('user.register', message=message))
    return render_template('register.html')

@user.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        u = User_operation()
        result = u.login(username, password)
        if result.json['code'] == 0:
            session['username'] = username
            session['user_id'] = session['username']
            message = result.json['message']
            return redirect(url_for('user.dashboard', message=message))
        else:
            message = result.json['message']
            return redirect(url_for('user.login', message=message))
    return render_template('login.html')

@user.route('/update_info', methods=['POST', 'GET'])
def update_info():
    if request.method == 'POST':
        data = request.form
        email = data['email']
        gender = data['gender']
        password = data['password'] if data['password'] else None

        username = session.get('username')
        if not username:
            flash('请先登录！', 'error')
            return redirect(url_for('user.login'))

        u = User_operation()
        result = u.update_info(username, email, gender, password)

        if result.json['code'] == 0:
            message = result.json['message']
            return redirect(url_for('user.dashboard', message=message))
        else:
            message = result.json['message']
            return redirect(url_for('user.update_info', message=message))

    username = session.get('username')
    if not username:
        flash('请先登录！', 'error')
        return redirect(url_for('user.login'))

    u = User_operation()
    user_info = u.get_user_info(username)
    return render_template('usercenter.html', user=user_info)

@user.route('/delete_account', methods=['POST', 'GET'])
def delete_account():
    if request.method == 'POST':
        username = session.get('username')
        if not username:
            flash('请先登录！', 'error')
            return redirect(url_for('user.login'))

        u = User_operation()
        result = u.delete_user(username)

        if result.json['code'] == 0:
            session.pop('username', None)
            message = result.json['message']
            return redirect(url_for('user.login', message=message))
        else:
            message = result.json['message']
            return redirect(url_for('user.login', message=message))

    return render_template('usercenter.html')

@user.route('/logout')
def logout():
    session.pop('username', None)
    flash('您已成功注销！', 'success')
    return redirect(url_for('user.login'))

@user.route('/dashboard')
def dashboard():
    return render_template('mrclassify.html')
