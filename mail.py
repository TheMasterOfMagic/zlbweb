from flask_mail import Mail, Message
from config import mail_config

app = None
mail = None


def init(_app):
    global app, mail
    app = _app
    app.config.update(mail_config)
    mail = Mail(app)


def send(title, recipients, html):
    message = Message(title, recipients, html=html)
    print(message)
    is_ok = True
    try:
        mail.send(message)
    except Exception:
        is_ok = False
    return is_ok


def test_mail(email):
    if email is None:  # 如果用户没有在地址栏里加email，提醒其加上
        return "<p>通过访问 <strong>/test_mail?email=【你的邮箱】</strong> 可以体验邮件发送功能喔~</p>"
        # 否则就正常发送邮件
    title = "体验邮件"
    recipients = [email]
    body = "<h1>恭喜你，邮件发送成功！</h1>"
    if send(title, recipients, body):  # 如果发送成功
        results = '<h1>邮件已发送，请查收~</h1>'
    else:  # 如果发送失败
        results = 'Whoops, looks like something went wrong'
    return results
