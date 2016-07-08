# coding=utf-8
from app import lm
from dbs import User
@lm.user_loader
def load_user(id):
    try:
        # 查询主键
        return User.query.get(id)
    except:
        return None

@lm.token_loader
def token_loader(token):
    try:
        return User.query.filter_by(token=token).first()
    except:
        return None