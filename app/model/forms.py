# coding=utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, email
class LoginForm(Form):
    username = StringField("用户名", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    remember = BooleanField("记住我")


class RegiForm(Form):
    username = StringField("用户名", validators=[Length(min=6, max=24)])
    email = StringField("邮箱", validators=[Length(min=6)])
    psd = PasswordField("密码", validators=[DataRequired(), EqualTo("rpsd", message="两次密码输入不一致")])
    rpsd = PasswordField("重复", validators=[DataRequired()])


class UserinfoForm(Form):
    userNickname = StringField("昵称", validators=[Length(min=3, max=20)])
    userEmail = StringField("邮箱", validators=[email()])
    userPhone = StringField("手机号", validators=[Length(min=0, max=11)])
    userBirthday = StringField("生日", validators=[Length(min=8, max=10)])
    userConstellation = StringField("星座", validators=[Length(min=3, max=6)])
    userGender = StringField("性别", validators=[Length(max=2)])

class PsdForm(Form):
    oldPsd = PasswordField("原密码", validators=[DataRequired()])
    newPsd = PasswordField("新密码", validators=[DataRequired(), EqualTo("rnewPsd", message="两次密码输入不一致")])
    rnewPsd = PasswordField("重复新密码", validators=[DataRequired()])

