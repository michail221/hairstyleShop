from app import db,login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    superuser = db.Column(db.Boolean, default=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    descrip = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer,nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    mainPhoto = db.Column(db.LargeBinary, nullable=True)
    secondPhoto = db.Column(db.LargeBinary, nullable=True)
    thirdPhoto = db.Column(db.LargeBinary, nullable=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Data = db.Column(db.DateTime, nullable=False)
    client = db.Column(db.String(100),nullable=False)
    item = db.Column(db.String(100),nullable=False)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
