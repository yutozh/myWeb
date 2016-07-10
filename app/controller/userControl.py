# coding=utf-8
import sys
import hashlib
import os
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import request, g, redirect, render_template
from flask.ext.login import login_required,logout_user
from flask_mail import Mail, Message
from app.model.dbs import *
from app.model.forms import *
from PIL import Image
from app.settings import content_body

@app.route("/updateUserInfo", methods=["POST"])
@login_required
def updateUserInfo():
    print request.form
    form = UserinfoForm(request.form)
    if form.validate_on_submit():
        g.user.nickname = form.userNickname.data
        g.user.email = form.userEmail.data
        g.user.birthday = form.userBirthday.data
        g.user.constellation = form.userConstellation.data
        g.user.phone = form.userPhone.data
        gender = request.form.get("userGender", "")
        if gender != "":
            g.user.gender = gender
        db.session.commit()
        send_mail("邮箱设置成功！",g.user.email,
            html=mail_body(content_body.format(username=g.user.username)))
    else:
        print form.errors
    return redirect("user/%s" % g.user.username)

@app.route("/updateUserImg", methods=["POST"])
@login_required
def updateUserImg():
    img = request.files["img"]
    try :
        x1 = int(request.form.get("x1",""))
        y1 = int(request.form.get("y1",""))
        x2 = int(request.form.get("x2",""))
        y2 = int(request.form.get("y2",""))
    except Exception as e:
        x1 = x2 = 0
        y1 = y2 = 100
    if img and allow_file(img.filename):
        m = hashlib.sha1()
        m.update(str(g.user.id))
        rnd = img.filename.rsplit(".", 1)[1]
        filename = m.hexdigest()[:20] + "." + rnd
        savepath = os.path.join(UPLOAD_FOLDER, "user_img/" + filename)

        error = ""
        dirname = os.path.dirname(savepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            img.save(savepath)
            im = Image.open(savepath)
            box = (x1, y1, x2, y2)
            aim = im.crop(box)
            aim.save(savepath)

            g.user.img = filename
            db.session.commit()
            return redirect("user/%s" % g.user.username)
    return redirect("user/%s" % g.user.username)

@app.route("/updateUserPsd", methods=["POST"])
@login_required
def updateUserPsd():
    form = PsdForm(request.form)
    if form.validate_on_submit():
        oldp = request.form.get("oldPsd")
        newp = request.form.get("newPsd")
        user = User(username=g.user.username, password=oldp)
        if user.is_authenticated():
            g.user.password = newp
            db.session.commit()
            alert = "密码修改成功,请重新登录！"
            logout_user()
            return render_template("Psdchanged.html", alert=alert)
        else:
            alert = "密码错误！！！"
    else:
        print form.errors
        alert = "表单错误！！！"
    return render_template("Psdchanged.html", alert=alert)

def allow_file(filename):
    return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENSIONS

def mail_body(body, foot="oattao.cn",subject="邮箱设置成功提醒",):
    body = render_template("mail_template.html",
                           subject=subject,
                           body=body,
                           foot=foot)
    return body

def send_mail(subject, email, body="", html=""):
    mail = Mail(app)

    msg = Message(subject=subject,
                  sender=app.config["MAIL_USERNAME"],
                  recipients=[email],
                  html=html)
    mail.send(msg)