from flask_mail import Mail, Message

app = None
mail = None


def init(_app):
    global app, mail
    app = _app
    app.config.update(dict(
        MAIL_DEBUG=True,
        MAIL_SERVER='smtp.163.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='zlbweb',
        MAIL_PASSWORD='jP8248SCk37qgMDr',
        MAIL_DEFAULT_SENDER='zlbweb.cn <zlbweb@163.com>'
    ))
    mail = Mail(app)


def send(title, recipients, html):
    message = Message(title, recipients, html=html)
    is_ok = True
    try:
        mail.send(message)
    except Exception:
        is_ok = False
    return is_ok
