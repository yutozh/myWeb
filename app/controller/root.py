# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import app, session, request, g, redirect,url_for, render_template
from flask.ext.login import login_required
from app.model.dbs import *
from app.model.loginmanager import *
import math
from config import POSTS_PER_PAGE_ADMIN
import json
@app.route("/root", methods=["POST","GET"])
@login_required
def root():
    if g.user.role == 0:
        return render_template("unable.html")
    if request.method == "POST":
        pass
    else:
        num_a = Article.query.filter_by(condition=1).count()
        num_p = len(Post.query.all())
        return render_template("root.html" ,user=g.user, num_a=num_a, num_p=num_p)

@app.route("/root/article", methods=["POST", "GET"])
@login_required
def root_article():
    if g.user.role == 0:
        return render_template("unable.html")
    if request.method == "GET":
        operation = request.args.get("operation", "")
        if operation == "review":
            aid = request.args.get("id","")
            aop = request.args.get("detail","")
            if aop in ['0','1','2']:
                a = Article.query.get(aid)
                a.condition = int(aop)
                db.session.commit()
        elif operation == "delete":
            aid = request.args.get("id","")
            a = Article.query.get(aid)
            db.session.delete(a)
            db.session.commit()
        elif operation == "getPages":
            all_pages = (int)(math.ceil(len(Article.query.all())))
            return (str)(all_pages)
    else:
        page = request.form.get("pages","1")
        posts = Article.query.filter(Article.id >= 0).order_by(-Article.timestamp).paginate(int(page), POSTS_PER_PAGE_ADMIN, False).items
        all_pages = (int)(math.ceil(len(Article.query.all()) * 1.0 / POSTS_PER_PAGE_ADMIN))
        innerHTML = render(posts)
        return json.dumps({"innerHTML": innerHTML, "pages": all_pages})
    return render_template("root_article.html" ,user=g.user)


@app.route("/root/user", methods=["POST", "GET"])
@login_required
def root_user():
    if g.user.role == 0:
        return render_template("unable.html")
    if request.method == "GET":
        operation = request.args.get("operation", "")
        if operation == "jurisdiction":
            uid = request.args.get("userid","")
            aop = request.args.get("detail","")
            u = User.query.get(uid)
            if aop == "up":
                u.role = g.user.role if (u.role + 1) > g.user.role else (u.role + 1)
                db.session.commit()
            elif aop == "down" and g.user.role > u.role:
                u.role = 0 if (u.role - 1) < 0 else (u.role - 1)
                db.session.commit()
        elif operation == "delete" and g.user.role == 2:
            uid = request.args.get("userid", "")
            u = User.query.get(uid)
            a = Article.query.filter_by(author=u).all()
            p = Post.query.filter_by(author=u).all()
            for i in a:
                db.session.delete(i)
            for i in p:
                db.session.delete(i)
            db.session.delete(u)
            db.session.commit()
        elif operation == "getPages":
            all_pages = (int)(math.ceil(len(User.query.all())))
            return (str)(all_pages)
    else:
        page = request.form.get("pages", "1")
        users = User.query.filter(User.id >= 0).order_by(-User.role).paginate(int(page), POSTS_PER_PAGE_ADMIN, False).items
        all_pages = (int)(math.ceil(len(User.query.all()) * 1.0 / POSTS_PER_PAGE_ADMIN))
        innerHTML = render2(users)
        return json.dumps({"innerHTML": innerHTML, "pages": all_pages})
    return render_template("root_user.html", user=g.user)


@app.route("/root/website", methods=["POST", "GET"])
@login_required
def root_website():
    success = ""
    if request.method == "POST" and g.user.role > 0:
        operation = request.form.get("operation","")
        content = request.form.get("content","")
        o = WebsiteConfig.query.filter_by(items=operation).first()
        if o is not None:
            o.content = content
            o.timestamp = datetime.datetime.now()
        else:
            o = WebsiteConfig(items=operation, content=content)
            db.session.add(o)
        db.session.commit()
        success = "设置成功!"
    return render_template("root_website.html", user=g.user, success=success)


@app.route("/root/post", methods=["POST", "GET"])
@login_required
def root_post():
    if g.user.role == 0:
        return render_template("unable.html")
    if request.method == "GET":
        operation = request.args.get("operation", "")
        if operation == "delete":
            pid = request.args.get("id","")
            p = Post.query.get(pid)
            db.session.delete(p)
            db.session.commit()
        elif operation == "getPages":
            all_pages = (int)(math.ceil(len(Post.query.all())))
            return (str)(all_pages)
    else:
        page = request.form.get("pages","1")
        posts = Post.query.filter(Post.id >= 0).order_by(-Post.timestamp).paginate(int(page), POSTS_PER_PAGE_ADMIN, False).items
        all_pages = (int)(math.ceil(len(Post.query.all()) * 1.0 / POSTS_PER_PAGE_ADMIN))
        innerHTML = render3(posts)
        return json.dumps({"innerHTML": innerHTML, "pages": all_pages})
    return render_template("root_post.html" ,user=g.user)


def render(posts):
    res = ""
    conList1 = ["label label-danger", "label label-info", "label label-success"]

    conList2 = ["未通过", "待审核", "已通过"]
    for post in posts:
        res += '''
                        <tr>
            <td>
                <a href="/article/{id}">{title}</a>
            </td>

            <td>{timestamp}</td>
            <td>{views}</td>

            <td>
                <span class="{condition1}">{condition2}</span>
            </td>
            <td>

                <button value="/root/article?operation=review&detail=2&id={id}" class="btn btn-mini blue"
                onclick="toConfirm(this);">
                    <i class="glyphicon glyphicon-ok-circle"></i> 通过
                </button>
                <button value="/root/article?operation=review&detail=0&id={id}" class="btn btn-mini black"
                onclick="toConfirm(this);">
                    <i class="glyphicon glyphicon-ban-circle"></i> 拒绝
                </button>
                <button value="/root/article?operation=delete&id={id}" class="btn btn-mini yellow"
                 onclick="toConfirm(this);">
                    <i class="glyphicon glyphicon-remove-circle"></i> 删除
                </button>
            </td>
        </tr>
        '''.format(id=post.id, title=post.title, timestamp=post.timestamp,
                   views=post.views, condition1=conList1[int(post.condition)], condition2=conList2[int(post.condition)])
    return res

def render2(users):
    res = ""
    conList1 = ["label label-primary", "label label-info", "label label-success"]

    conList2 = ["普通用户", "管理员", "站长"]
    for user in users:
        articles = Article.query.filter_by(author=user)
        num_a = articles.count()
        num_view = 0
        for a in articles:
            num_view += a.views
        res += '''
                        <tr>
            <td>
                <a href="/user/{username}">{username}</a>
            </td>

            <td>{timestamp}</td>
            <td>{num_a}</td>
            <td>{num_view}</td>
            <td>
                <span class="{condition1}">{condition2}</span>
            </td>
            <td>

                <button value="/root/user?operation=jurisdiction&detail=up&userid={id}" class="btn btn-mini blue"
                onclick="toConfirm(this);">
                    <i class="glyphicon glyphicon-ok-circle"></i> 提高权限
                </button>
                <button value="/root/user?operation=jurisdiction&detail=down&userid={id}" class="btn btn-mini black"
                  onclick="toConfirm(this);">
                    <i class="glyphicon glyphicon-ban-circle"></i> 降低权限
                </button>
                <button value="/root/user?operation=delete&userid={id}" class="btn btn-mini yellow"
                   onclick="toConfirm(this);">
                    <i class="glyphicon glyphicon-remove-circle"></i> 删除用户
                </button>
            </td>
        </tr>
        '''.format(id=user.id, username=user.username, timestamp=user.timestamp,
                   num_a=num_a, num_view=num_view, condition1=conList1[int(user.role)], condition2=conList2[int(user.role)])
    return res

def render3(posts):
    res = ""
    for post in posts:
        res += '''
                            <tr>
                <td>
                    <div class="success">{body}</div>
                </td>

                <td>{timestamp}</td>
                <td>{author}</td>

                <td>
                    <button value="/root/post?operation=delete&id={id}" class="btn btn-mini yellow"
                     onclick="toConfirm(this);">
                        <i class="glyphicon glyphicon-remove-circle"></i> 删除
                    </button>
                </td>
            </tr>
            '''.format(id=post.id, body=post.body, timestamp=post.timestamp, author=post.author)
    return res