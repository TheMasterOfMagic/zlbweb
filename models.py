from flask_login import UserMixin

from database import db


# user models
class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column(db.INT)
    username = db.Column(db.String(45))
    email = db.Column(db.String(128), primary_key=True)
    password = db.Column(db.String(512))
    salt = db.Column(db.String(64))
    access_token = db.Column(db.String(128))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def verify_password(self, password):
        return self.password == password

    def __repr__(self):
        return '<User %r>' % self.username



class FileHash(db.Model,UserMixin):
    __tablename__ = 'FileHash'

    filename = db.Column(db.String(50), primary_key=True)
    hash = db.Column(db.String(512))

