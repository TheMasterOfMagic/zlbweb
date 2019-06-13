from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo


class DownloadForm(FlaskForm):
    filename = StringField('filename',validators=[DataRequired()])
