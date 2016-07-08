# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from app import app
from flask import app, session, request, g,render_template, redirect, url_for
from geetest import GeetestLib
from flask.ext.login import login_required,login_user
from app.model.dbs import *
from app.model.loginmanager import *
from app.model.forms import *
from config import captcha_id, private_key
import datetime
import json

@app.route('/register', methods=["GET"])
def get_captcha():
    # user_id = 'test'
    gt = GeetestLib(captcha_id, private_key)
    status = gt.pre_process()
    session[gt.GT_STATUS_SESSION_KEY] = status
    response_str = gt.get_response_str()
    return response_str

@app.route('/validate', methods=["POST", "GET"])
@login_required
def validate_capthca():
    gt = GeetestLib(captcha_id, private_key)
    challenge = request.form[gt.FN_CHALLENGE]
    validate = request.form[gt.FN_VALIDATE]
    seccode = request.form[gt.FN_SECCODE]
    status = session[gt.GT_STATUS_SESSION_KEY]

    if status:
        result = gt.success_validate(challenge, validate, seccode)
    else:
        result = gt.failback_validate(challenge, validate, seccode)

    return result

@app.route('/ajax_validate', methods=["POST"])
def ajax_validate():
    gt = GeetestLib(captcha_id, private_key)
    challenge = request.form[gt.FN_CHALLENGE]
    validate = request.form[gt.FN_VALIDATE]
    seccode = request.form[gt.FN_SECCODE]
    status = session[gt.GT_STATUS_SESSION_KEY]

    if status:
        result = gt.success_validate(challenge, validate, seccode)
    else:
        result = gt.failback_validate(challenge, validate, seccode)

    return result

    # if result:
    #     aim = request.form.get("aim", "")
    #     if not g.user.is_authenticated and aim == "login":
    #         result = {}
    #         result["status"] = "success"
    #         form = LoginForm(request.form)
    #         if request.method == 'POST' and form.validate_on_submit():
    #             user = User(username=form.username.data, password=form.password.data)
    #             if user.is_authenticated():
    #                 user = User.query.filter_by(username=form.username.data).first()
    #                 if request.form.get("remember", "") == 'true':
    #                     login_user(user, remember=True)
    #                 else:
    #                     login_user(user, remember=False)
    #                 result["login_res"] = "ok"
    #             else:
    #                 result["login_res"] = "用户名或密码错误"
    #         else:
    #             result["login_res"] = "非法输入"
    #         return json.dumps(result)
    #     if g.user is not None and aim == "":
    #         if request.method == "POST":
    #             title = request.form.get("title", "")
    #             body = request.form.get("body", "")
    #             type = request.form.get("type", "")
    #             if title != "" and body != "" and type != "":
    #                 a = Article(title=title, body=body,
    #                             timestamp=datetime.datetime.now(), tags=type,
    #                             author=g.user)
    #                 db.session.add(a)
    #                 db.session.commit()
    #             else:
    #                 result = False
    #
    # result = {"status":"success"} if result else {"status":"fail"}
    # return json.dumps(result)

@app.route("/login",methods=["POST"])
def login():
    result = ajax_validate()
    if result:
        aim = request.form.get("aim", "")
        if not g.user.is_authenticated and aim == "login":
            result = {}
            result["status"] = "success"
            form = LoginForm(request.form)
            if request.method == 'POST' and form.validate_on_submit():
                user = User(username=form.username.data, password=form.password.data)
                if user.is_authenticated():
                    user = User.query.filter_by(username=form.username.data).first()
                    if request.form.get("remember", "") == 'true':
                        login_user(user, remember=True)
                    else:
                        login_user(user, remember=False)
                    result["login_res"] = "ok"
                else:
                    result["login_res"] = "用户名或密码错误"
            else:
                result["login_res"] = "非法输入"
            return json.dumps(result)
    else:
        result = {"status": "fail"}
        return json.dumps(result)