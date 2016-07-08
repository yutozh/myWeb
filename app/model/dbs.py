# coding=utf-8
from app import app, db
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import make_secure_token
from flask import Flask
from werkzeug import security
import datetime
ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_ROOT = 2

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128), unique=False)
    password_salt = db.Column(db.String(64))
    token = db.Column(db.String(128))
    timestamp = db.Column(db.Date)
    nickname = db.Column(db.String(64))
    img = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(128), unique=True)
    gender = db.Column(db.Integer, default=-1) # -1 unknown 0 male 1 female
    birthday = db.Column(db.Date)
    constellation = db.Column(db.String(10))
    phone = db.Column(db.String(15))
    money = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)
    area = db.Column(db.String(128),default="")
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    articles = db.relationship("Article", backref="author", lazy="dynamic")

    __PassWord_Method = "pbkdf2:sha1:1000"

    # def __init__(self, username, password):
    #     self.username = username
    #     self.password = password
    #
    #     # 生成密码的hash值 和 salt值，存储在数据库中
    #     temp_password = security.generate_password_hash(password, salt_length=32)
    #     self.password_salt, self.password_hash = temp_password.split('$')[1:3]

    # def __init__(self):
    #     temp_password = security.generate_password_hash(password, salt_length=32)
    #     self.password_salt, self.password_hash = temp_password.split('$')[1:3]
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value
        # 生成密码的hash值 和 salt值，存储在数据库中
        temp_password = security.generate_password_hash(value, salt_length=32)
        self.password_salt, self.password_hash = temp_password.split('$')[1:3]

    def is_authenticated(self):
        user = User.query.filter_by(username=self.username).first()

        if user is not None and self.check_password(user):
            return True
        else:
            return False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def check_password(self, user):
        temp_password = [User.__PassWord_Method, user.password_salt, user.password_hash]
        link_str = "$"
        return security.check_password_hash(link_str.join(temp_password), self.password)

    # 返回标记该用户的令牌
    def get_auth_token(self):
        self.token = make_secure_token(self.password_hash, self.username)
        return self.token

    def __repr__(self):
        return "<User: %s>" % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    username = db.Column(db.String(64), db.ForeignKey("user.username"))

    def __repr__(self):
        return "<Post: %s>" % (self.body)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    body = db.Column(db.String(10000), nullable=False)
    timestamp = db.Column(db.DateTime)
    type= db.Column(db.String(60))
    username = db.Column(db.String(64), db.ForeignKey("user.username"))
    permission = db.Column(db.Integer, default=0)
    pros = db.Column(db.Integer, default=0)
    cons = db.Column(db.Integer, default=0)
    condition = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)

class IP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.String(64))
    article_id = db.Column(db.Integer, nullable=False)

class WebsiteConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    items = db.Column(db.String(256))
    content = db.Column(db.Text)