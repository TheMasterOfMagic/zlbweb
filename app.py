from flask import Flask, request
import mail
import file
from flask import render_template, redirect, url_for, request
from forms.signin_form import LoginForm
from forms.signup_form import RegisterForm
from forms.dowmload_form import DownloadForm
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_login import LoginManager, login_required, login_user, logout_user,current_user
import config

from database import create_app, add_user
from models import User
import signinup

app = create_app()
# 防止跨站脚本攻击
app.secret_key = config.secretinfo['secret_key']
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB
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
    #return User.query.get(int(userid))
    return User.query.filter_by(id=userid).first()


@app.route('/')
def index():
    return render_template('index.html')


# ------------------------------------------------------退出登录部分代码----------------------------
@app.route('/signoff')
@login_required
def signoff():
    logout_user()
    return redirect(url_for('index'))


# ----------------------------------------------------注册部分的代码-----------------------------------
@app.route('/signin', methods=['GET'])
def signin():
    form = LoginForm()
    return render_template('./login/signup.html', form=form)


@app.route('/signin', methods=['POST'])
def do_signin():
    html = signinup.signin_User()
    return html


# --------------------------------------------登陆部分的代码-------------------------------------------
@app.route('/signup', methods=['GET'])
def signup():
    form = RegisterForm()
    return render_template('./login/signin.html', form=form)


@app.route('/signup', methods=['POST'])
def do_signup():
    html = signinup.signup_User()
    return html


@csrf.exempt
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('./csrf/csrf_error.html', reason=e.description), 400


@app.route('/test_mail')
def test_mail():
    email = request.args.get('email')
    return mail.test_mail(email)


@app.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    print(current_user.is_anonymous)
    f=file.upload_file()
    return f


# 文件下载页面
@app.route('/filedownload', methods=['GET'])
def filedownload():
    form = DownloadForm()
    return render_template('./upload/download.html',form=form)

@app.route('/filelist', methods=['GET','POST'])
def filelist():
    filelist = file.file_list()
    return filelist


@app.route('/download', methods=['GET', 'POST'])
def download():
    form = DownloadForm()
    filename = form.filename.data
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return file.download(filename)
    return file.download_anonmity(filename)

def main():
    mail.init(app)
    file.init(app)
    app.run(host='zlbweb.cn', port=443, ssl_context=('cert.pem', 'key.pem'))


if __name__ == "__main__":
    main()
