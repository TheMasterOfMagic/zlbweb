from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo


class LoginForm(FlaskForm):
    userName = StringField('password', validators=[DataRequired(),
                                                   Regexp('^[A-Za-z0-9\u4e00-\u9fa5]+$', 0,
                                                          message="用户名字只能包含中文，英文字母，数字")])
    email = StringField('email', validators=[DataRequired(), Email(message="邮箱格式有误")])
    # 密码必须包含大写、小写、数字，且至少出现一次
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=32),
                                                     Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', 0,
                                                            "密码长度限制在3~36之间且密码不能为弱密码"),
                                                     EqualTo('confirmpassword', message='Passwords must match')],)
    confirmpassword = PasswordField('confirmpassword')