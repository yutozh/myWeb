# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import redirect, g, request, url_for, make_response
from flask.ext.login import  logout_user, current_user, login_required
from app.model.forms import *
from app.model.dbs import *
from app.controller.weberrors import *
from config import POSTS_PER_PAGE, POSTS_PER_PAGE_ADMIN, POSTS_CHAT_PER_PAGE
import math
import datetime
import json
import cgi

db.create_all()

@app.before_request
def before_login():
    g.user= current_user

@app.route("/", methods=["POST", "GET"])
@app.route("/<int:page>", methods=["POST", "GET"])
def default(page=""):
    if page:
        return redirect(("home/{}".format(page)))
    else:
        return redirect("home")

@app.route("/home/<int:page>", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home(page=1):
    if page <1:
        return redirect("home/1")
    alert = WebsiteConfig.query.filter_by(items="home-alert").first()
    jumbotron = WebsiteConfig.query.filter_by(items="home-jumbotron").first()
    notify = WebsiteConfig.query.filter_by(items="home-notify").first()
    articles = Article.query.filter_by(condition=2).order_by(-Article.timestamp).paginate(page, POSTS_PER_PAGE, False).items
    all_pages = (int)(math.ceil((Article.query.filter(Article.id>-1).count()) * 1.0 / POSTS_PER_PAGE))
    if articles is None:
        articles = "暂时还没有文章哦～～～"
    form = LoginForm(request.form)
    if g.user is not None and g.user.is_authenticated:
        form = None
    return render_template("home.html", pages=(all_pages, page),alert=alert, jumbotron=jumbotron,
                          notify=notify, form=form, user=g.user, articles=articles)

@app.route("/regi", methods=["POST"])
def regi():
    form = RegiForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data,
        username=form.username.data, password=form.psd.data)
        db.session.add(user)
        db.session.commit()
        return render_template("home.html", form=form, user=None)
    print form.errors
    return render_template("home.html", form=form, error=form.errors.values()[0], user=None)

@app.route("/loginout")
@login_required
def loginout():
    logout_user()
    resp = make_response(redirect(url_for('home')))
    return resp

@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for("home"))
    (isMe, form, form_p) = (True, UserinfoForm(), PsdForm()) if user == g.user else (False, None, None)
    imgFilename = user.img
    return render_template("user.html", user=user, isMe=isMe ,form=form, user_img_id=imgFilename, form_p=form_p)

@app.route("/ajax_page_change", methods=["GET","POST"])
@login_required
def page_change():
    # GET获取总数
    if request.method == "GET":
        username = request.args.get("username", "")
        all_pages = (int)(math.ceil(Article.query.filter_by(username=username).count()))
        return (str)(all_pages)
    # POST获取指定页条目
    page = request.form.get("page",1)
    type = request.form.get("type", "")
    username = request.form.get("username", "")
    if type == "section-article-manage":
        posts = Article.query.filter_by(username=username).paginate(int(page), POSTS_PER_PAGE_ADMIN, False).items
        innerHTML = render(posts)
        return json.dumps({"innerHTML":innerHTML})

# 留言板读取
@app.route("/ajax_post_get", methods=["POST"])
def post_get():
    page = request.form.get("page",1)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(int(page), POSTS_CHAT_PER_PAGE, False).items
    isEnd = False if len(posts) == POSTS_CHAT_PER_PAGE else True
    res = []
    for i in posts:
        temp = {}
        temp["authorimg"] = i.author.img
        temp["author"] = i.author.username
        temp["body"] = i.body
        temp["timestamp"] = str(i.timestamp).split(" ")[0]
        res.append(temp)
    result = {}
    result["content"] = res
    result["isEnd"] = isEnd

    return json.dumps(result)

# 留言板添加
@app.route("/ajax_post_add", methods=["POST"])
@login_required
def post_add():
    content = cgi.escape(request.form.get("content",""))
    if content !="" and len(content)<=140:
        i = Post(body=content, timestamp = datetime.datetime.now(), author=g.user)
        temp = {}
        temp["authorimg"] = i.author.img
        temp["author"] = i.author.username
        temp["body"] = i.body
        temp["timestamp"] = str(i.timestamp).split(" ")[0]
        db.session.add(i)
        db.session.commit()
        return json.dumps({"result":"success", "content": temp})
    return json.dumps({"result":"fail"})

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
                                <a href="/edit?id={id}" class="btn btn-mini purple">
                                    <i class="glyphicon glyphicon-edit"></i> 编辑
                                </a>
                                <button class="btn btn-mini yellow" type="button"
                                onclick="toClose('/delete?id={id}')">
                                    <i class="glyphicon glyphicon-remove"></i> 删除
                                </button>
                            </td>
                        </tr>
        '''.format(id=post.id, title=post.title, timestamp=post.timestamp, views=post.views,
                   condition1=conList1[int(post.condition)], condition2=conList2[int(post.condition)])
    return res

def delete():
    article = Article.query.all()
    for a in article:
        db.session.delete(a)

    posts = Post.query.all()
    for p in posts:
        db.session.delete(p)
    users = User.query.all()
    for u in users:
        db.session.delete(u)

    db.session.commit()

