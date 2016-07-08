# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
from app.model.dbs import *
import app.settings as settings
from flask import render_template, redirect,g, request, make_response, url_for, session
from flask.ext.login import login_required
from app.model.forms import *
import datetime
import json
import random
from app.controller.weberrors import *
import thread
import time
import cgi

@app.route("/article/<int:num>")
def article(num):
    article = Article.query.filter_by(id=num).first()
    form = LoginForm()
    if article is not None:
        if article.condition == 2 or g.user.role > 0 or article.author == g.user:
            article.views += 1
            db.session.commit()
            return render_template("article.html", article=article, user=g.user, form=form)
    return redirect(error_404)

@app.route("/edit", methods=["POST", "GET"])
@login_required
def edit():
    if request.method == "GET":
        search = request.args.get("id","")
        article = Article.query.get(search)
        if article is not None:
            if article.author == g.user:
                session["article_id"] = search
                return render_template("edit.html", user=g.user, tags=settings.article_types, article=article)
            else:
                return render_template("unable.html")
        else:
            return render_template("edit.html", user=g.user, tags=settings.article_types)

    if request.method == "POST":
        from validate import ajax_validate
        if ajax_validate():
            title = cgi.escape(request.form.get("title", ""))
            body = request.form.get("body", "")
            type = request.form.get("type", "")
            if title != "" and body != "" and type != "":
                try:
                    artToChange = session["article_id"]
                    if artToChange:
                        session["article_id"] = ""
                        a = Article.query.get(artToChange)
                        a.title = title
                        a.body = body
                        a.type = type
                        a.timestamp = datetime.datetime.now()
                    else:
                        a = Article(title=title, body=body,
                                    timestamp=datetime.datetime.now(), type=type,
                                    author=g.user, condition=1)
                        db.session.add(a)
                except:
                    a = Article(title=title, body=body,
                                timestamp=datetime.datetime.now(), type=type,
                                author=g.user, condition=1)
                    db.session.add(a)
                finally:
                    db.session.commit()
                    result = {"status": "success"}
            else:
                result = {"status":"fail"}
        else:
            result = {"status": "fail"}
        return json.dumps(result)

@app.route("/delete", methods=["GET"])
@login_required
def deleteArticle():
    article_id = request.args.get("id","")
    article = Article.query.get(article_id)
    if g.user == article.author:
        db.session.delete(article)
        db.session.commit()
    return redirect(url_for('user',username=g.user.username))

@app.route("/pc_count", methods=["POST"])
def pc_count():
    value = request.form.get("type","")
    article_id = request.form.get("id","")
    article = Article.query.filter_by(id=article_id).first()

    if value == "init":
        result = {"success": 1, "value": [article.pros, article.cons]}
        return json.dumps(result)

    ip = request.remote_addr
    if IP.query.filter_by(ip_address = ip, article_id=article_id).first() is not None:
        result = {"success":0,"value":["你今天已经投过票啦>_<",]}
    else:
        new_ip = IP(article_id=article_id, ip_address=ip)
        db.session.add(new_ip)
        if value == "pros":
            article.pros += 1
            result = {"success": 1, "value": [article.pros,]}
        else:
            article.cons += 1
            result = {"success": 1, "value": [article.cons,]}
        db.session.commit()
    return json.dumps(result)

@app.route('/ckupload/', methods=["POST"])
@login_required
def ckupload():
    error = ''
    url = ''
    filelocation = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        if fext in [".jpg", ".png", ".gif", ".bmp"]:
            filelocation = "upload/images"
        else:
            filelocation = "upload/files"
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(app.static_folder, filelocation, rnd_name)
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % (filelocation, rnd_name))
    else:
        error = 'post error'
    res = """

<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>

""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))

def delete_ip():
    while (True):
        ips = IP.query.all()
        for i in ips:
            db.session.delete(i)
        db.session.commit()
        time.sleep(3600*24)

t = thread.start_new(delete_ip,())