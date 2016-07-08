# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import random
import datetime
app = Flask(__name__)
db = SQLAlchemy(app)
from app.model.dbs import *
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def add_posts():
    for i in range(10):
        p = Post(body=str(random.random()*random.random()),
             timestamp = datetime.datetime.now(),
             author=User(username=str(random.random())))
        db.session.add(p)
    db.session.commit()
    print "success"

@manager.option('-u','--username',dest='username', default="Default")
@manager.option('-p','--password',dest='password', default="Default")
def add_user(username, password):
    u = User(username=username, password=password)
    try:
        db.session.add(u)
        db.session.commit()
        print "完成"
    except:
        print "用户名重复"

if __name__ == '__main__':
    manager.run()
