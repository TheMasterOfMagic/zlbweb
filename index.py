from flask import Flask, render_template
from forms import LoginForm
from flask_wtf.csrf import CSRFProtect, CSRFError

app = Flask("YY")
app.secret_key = 'zlbweb'
# app.config['WTF_CSRF_SECRET_KEY'] = 'CSRFTokenGeneratorSecretKey2018' # CSRF Token生成器的签发密钥
# app.config['WTF_CSRF_TIME_LIMIT'] = 10 # 表单提交限时1分钟，超时则触发CSRF Token校验失败错误
csrf = CSRFProtect(app)

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
        if form.email.data == '384861882@qq.com' and form.password.data == 'zlbweb':
            return render_template('welcome.html', userName=form.userName.data)
        else:
            return render_template('signup.html', form=form, message='password and user name mismatch, login failed')
    else:
        if form.errors.get('userName', 'None')[0] == "用户名字只能包含中文，英文字母，数字" :
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
