from flask import Flask, request
import mail
import file
from flask import render_template, redirect, url_for, request
from forms.signin_form import LoginForm
from forms.signup_form import RegisterForm
from flask_wtf.csrf import CSRFProtect, CSRFError
from werkzeug.exceptions import HTTPException, NotFound
from flask_login import LoginManager, login_required, login_user, logout_user

import os
import config

from database import create_app, add_user
from models import User

app = create_app()
# 防止跨站脚本攻击
app.secret_key = config.secretinfo['secret_key']
# app.config['WTF_CSRF_SECRET_KEY'] = 'CSRFTokenGeneratorSecretKey2018' # CSRF Token生成器的签发密钥
# app.config['WTF_CSRF_TIME_LIMIT'] = 10 # 表单提交限时1分钟，超时则触发CSRF Token校验失败错误
csrf = CSRFProtect(app)

# Add LoginManager
login_manager = LoginManager()
login_manager.session_protection = config.secretinfo['login_manager_session_protection']
login_manager.login_view = config.secretinfo['login_manager_login_view']
login_manager.login_message = config.secretinfo['login_manager_login_message']
login_manager.login_message_category = config.secretinfo['login_manager_login_message_category']
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
def index():
    return render_template('index.html')


# ------------------------------------------------------退出登录部分代码----------------------------
@app.route('/signoff')
@login_required
def signoff():
    logout_user()
    return 'Logged out successfully!'


# ----------------------------------------------------注册部分的代码-----------------------------------
@app.route('/signin', methods=['GET'])
def signin():
    form = LoginForm()
    return render_template('./login/signup.html', form=form)


@app.route('/signin', methods=['POST'])
def do_signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            # next = request.args.get('next')
            # return redirect(next or url_for('welcome'))
            return render_template('./login/signup.html', form=form, message="该邮箱已被注册")
        else:
            login_user(user)
            id = (User.query.order_by((User.id).desc()).first()).id + 1
            add_user(form, id)
            next = request.args.get('next')
            return redirect(next or url_for('upload'))
            # return render_template('welcome.html', form=form, userName=form.userName.data)
    else:
        return render_template('./login/signup.html', form=form, message=list(form.errors.values())[0][0])


# --------------------------------------------登陆部分的代码-------------------------------------------
@app.route('/signup', methods=['GET'])
def signup():
    form = RegisterForm()
    return render_template('./login/signin.html', form=form)


@app.route('/signup', methods=['POST'])
def do_signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('upload'))
            # return render_template('welcome.html', form=form, userName=user.username)
        else:
            return render_template('./login/signin.html', form=form, message='账户或者密码错误')
    else:
        return render_template('./login/signin.html', form=form, message='账户或者密码错误')


@csrf.exempt
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('./csrf/csrf_error.html', reason=e.description), 400


@app.route('/test_mail')
def test_mail():
    email = request.args.get('email')
    return mail.test_mail(email)


# <<<<<<< HEAD
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    return file.upload_file()


# =======
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    f = file.upload_file()
    return f


# >>>>>>> d4ddbba3eae3c1884ba6159ef206fba546ce4708


@app.route('/file_list', methods=['GET', 'POST'])
def file_list():
    filelist = file.file_list()
    return file.download_file(filelist)


def main():
    mail.init(app)
    file.init(app)
    app.run(host='zlbweb.cn', port=443, ssl_context=('cert.pem', 'key.pem'))


if __name__ == "__main__":
    main()
