from flask_login import UserMixin

from database import db


# user models
class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column(db.INT)
    username = db.Column(db.String(45))
    email = db.Column(db.String(128), primary_key=True)
    password = db.Column(db.String(512))
    access_token = db.Column(db.String(128))

    def verify_password(self, password):
        return self.password == password

    def __repr__(self):
        return '<User %r>' % self.username
