from model.user import User
from flask import jsonify
from db_config import db_init as db

class User_operation():
    def __init__(self):
        super().__init__()

    def login(self, username, password):
        u = User.query.filter_by(username=username).first()
        if u is None:
            return jsonify({'code': -1, 'message': '用户不存在', 'data': {}})

        u_dict = u.to_dict()
        if u_dict['password'] != password:
            return jsonify({'code': -2, 'message': '密码错误', 'data': {}})

        return jsonify({'code': 0, 'message': '登录成功', 'data': u_dict})

    def register(self, username, email, gender, password):
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'code': -1, 'message': '用户名已存在！', 'data': {}})
        if existing_email:
            return jsonify({'code': -2, 'message': '邮箱已被注册！', 'data': {}})
        new_user = User(username=username, email=email, gender=gender, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'code': 0, 'message': '注册成功！', 'data': new_user.to_dict()})

    def update_info(self, username, email, gender, password):
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'code': -1, 'message': '用户不存在！', 'data': {}})
        user.email = email
        user.gender = gender
        if password:
            user.password = password
        db.session.commit()

        return jsonify({'code': 0, 'message': '信息更新成功！', 'data': user.to_dict()})

    def delete_user(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'code': -1, 'message': '用户不存在！', 'data': {}})

        db.session.delete(user)
        db.session.commit()
        return jsonify({'code': 0, 'message': '用户账号删除成功！', 'data': {}})

    def get_user_info(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return None
        return user.to_dict()
