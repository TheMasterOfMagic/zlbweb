from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@39.105.62.149:3306/zlbweb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    with app.app_context():
        from models import User
        db.create_all()
        db.session.merge(User(id=0,username="lycheng", email='anjing@cuc.edu.cn', password='aB8'))
        db.session.commit()
    return app

def add_user(user,userID):
    from models import User
    db.session.add(User(id=userID,username=user.userName.data, email=user.email.data, password=user.password.data))
    db.session.commit()
