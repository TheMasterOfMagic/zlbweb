from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp
import re

class LoginForm(FlaskForm):
    userName = StringField('password', validators=[DataRequired(),
                                                   Regexp('^[A-Za-z0-9\u4e00-\u9fa5]+$', 0,
                                                          message="用户名字只能包含中文，英文字母，数字")])
    email = StringField('email', validators=[DataRequired(), Email()])
    # 密码必须包含大写、小写、数字，且至少出现一次
    password = PasswordField('password', validators=[DataRequired(), Length(min=3, max=36),
                                                     Regexp('([A-Z]+[a-z]+[0-9]+[\\d\\w]*)|([A-Z]+[0-9]+[a-z]+[\\d\\w]*)'
                                                            '|([0-9]+[a-z]+[A-Z]+[\\d\\w]*)" +"|([0-9]+[A-Z]+[a-z]+[\\'
                                                            'd\\w]*)|([a-z]+[0-9]+[A-Z]+[\\d\\w]*)|([a-z]+[A-Z]+[0-9]+[\\'
                                                            'd\\w]*)', 0,
                                                            "密码长度限制在3~36之间且密码不能为弱密码")],)



