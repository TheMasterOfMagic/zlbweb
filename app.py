from flask import Flask, request
import mail

app = Flask(__name__)


@app.route('/test_mail')
def index():
    email = request.args.get('email')
    if email is None:  # 如果用户没有在地址栏里加email，提醒其加上
        return "<p>通过访问 <strong>/test_mail?mail=【你的邮箱】</strong> 可以体验邮件发送功能喔~</p>"
    # 否则就正常发送邮件
    title = "体验邮件"
    recipients = [email]
    body = "<h1>恭喜你，邮件发送成功！</h1>"
    if mail.send(title, recipients, body):  # 如果发送成功
        results = '<h1>邮件已发送，请查收~</h1>'
    else:  # 如果发送失败
        results = 'Whoops, looks like something went wrong'
    return results


def main():
    mail.init(app)
    app.run(host='zlbweb.cn', port=443, ssl_context=('cert.pem', 'key.pem'))


if __name__ == "__main__":
    main()
