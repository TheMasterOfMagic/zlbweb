from flask import render_template, redirect, url_for, request
from forms.signin_form import LoginForm
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_login import LoginManager, login_required, login_user, logout_user

import os

from database import create_app,add_user
from models import User

app = create_app()
app.secret_key = 'zlbweb'
# app.config['WTF_CSRF_SECRET_KEY'] = 'CSRFTokenGeneratorSecretKey2018' # CSRF Token生成器的签发密钥
# app.config['WTF_CSRF_TIME_LIMIT'] = 10 # 表单提交限时1分钟，超时则触发CSRF Token校验失败错误
csrf = CSRFProtect(app)

# Add LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'AdminPassword4Me'
login_manager.login_view = 'signin'
login_manager.login_message = 'Unauthorized User'
login_manager.login_message_category = "info"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin', methods=['GET'])
def signin():
    form = LoginForm()
    return render_template('signup.html', form=form)


@app.route('/signin', methods=['POST'])
def do_signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            # next = request.args.get('next')
            # return redirect(next or url_for('welcome'))
            return render_template('signup.html', form=form, message="该邮箱已被注册")
        else:
            id = (User.query.order_by((User.id).desc()).first()).id +1
            add_user(form,id)
            return render_template('welcome.html', form=form, userName=form.userName.data)
    else:
        if form.errors.get('userName', 'None')[0] == "用户名字只能包含中文，英文字母，数字":
            return render_template('signup.html', form=form, message="用户名字只能包含中文，英文字母，数字")
        elif form.errors.get('password', 'None')[0] == "密码长度限制在3~36之间且密码不能为弱密码":
            return render_template('signup.html', form=form, message="密码长度限制在3~36之间且密码不能为弱密码")
        else:
            return render_template('signup.html', form=form, message='邮箱格式有问题')


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400


if __name__ == '__main__':
    app.run(host='zlbweb.cn', port=443, ssl_context=('cert.pem', 'key.pem'))
