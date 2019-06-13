from flask import render_template, redirect, url_for, request,g
from forms.signin_form import LoginForm
from forms.signup_form import RegisterForm
from flask_login import  login_user
from database import create_app, add_user
from models import User
import hashlib

# 注册新用户
def signin_User():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            # next = request.args.get('next')
            # return redirect(next or url_for('welcome'))
            return render_template('./login/signup.html', form=form, message="该邮箱已被注册")
        else:
            # login_user(user)

            # 使用sha512进行hash
            hash = hashlib.sha512()
            # 将盐值和密码进行拼接
            hashpassword = form.salt.encode() + form.password.data.encode()
            hash.update(hashpassword)
            form.password.data = hash.hexdigest()

            try:
                id = (User.query.order_by((User.id).desc()).first()).id + 1
            except AttributeError:
                id = 0

            add_user(form, id)
            next = request.args.get('next')
            return redirect(next or url_for('upload_file'))
            # return render_template('welcome.html', form=form, userName=form.userName.data)
    else:
        return render_template('./login/signup.html', form=form, message=list(form.errors.values())[0][0])

# 用户登录
def signup_User():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        resulthash = ""
        if user is not None:
            # 检测密码是否正确
            hash = hashlib.sha512()
            # 将盐值和密码进行拼接
            hashpassword = user.salt + form.password.data.encode()
            hash.update(hashpassword)
            resulthash = hash.hexdigest()

        if user is not None and user.verify_password(resulthash):
            # 启动用户登录

            current_user = User()
            current_user.id = user.id
            login_user(current_user)
            next = request.args.get('next')
            return redirect(next or url_for('upload_file'))
        else:
            return render_template('./login/signin.html', form=form, message='账户或者密码错误')
    else:
        return render_template('./login/signin.html', form=form, message='账户或者密码错误')