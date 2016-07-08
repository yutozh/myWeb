# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from app.model.dbs import *
from flask import render_template, g, request
from config import POSTS_PER_PAGE
import math
from app.model.forms import LoginForm
@app.route("/notes")
@app.route("/notes/<int:page>")
def notes(page=1):
    form = LoginForm()
    page = (int)(request.args.get("page", 1))
    notify = WebsiteConfig.query.filter_by(items="note-notify").first()
    articles = Article.query.filter_by(type = "学习笔记", condition=2).order_by(-Article.timestamp).paginate(page, POSTS_PER_PAGE, False).items
    all_pages = (int)(math.ceil(Article.query.filter_by(type = "学习笔记").count() * 1.0 / POSTS_PER_PAGE))
    articles = "" if len(articles) == 0 else articles
    return render_template("notes.html", articles=articles, notify=notify,
                           pages=(all_pages,page), user=g.user, form=form)

@app.route("/reading")
@app.route("/reading/<int:page>")
def reading(page=1):
    form = LoginForm()
    page = (int)(request.args.get("page",1))
    articles = Article.query.filter_by(type = "读书笔记",condition=2).order_by(-Article.timestamp).paginate(page, POSTS_PER_PAGE, False).items
    notify = WebsiteConfig.query.filter_by(items="reading-notify").first()
    all_pages = (int)(math.ceil(Article.query.filter_by(type = "读书笔记").count() * 1.0 / POSTS_PER_PAGE))
    articles = "" if len(articles) == 0 else articles
    return render_template("reading.html", articles=articles, notify=notify,
                           pages=(all_pages, page), user=g.user, form=form)

@app.route("/mood")
@app.route("/mood/<int:page>")
def mood(page=1):
    form = LoginForm()
    page = (int)(request.args.get("page", 1))
    articles = Article.query.filter_by(type = "心情",condition=2).order_by(-Article.timestamp).paginate(page, POSTS_PER_PAGE, False).items
    notify = WebsiteConfig.query.filter_by(items="mood-notify").first()
    all_pages = (int)(math.ceil(Article.query.filter_by(type = "心情").count() * 1.0 / POSTS_PER_PAGE))
    articles = "" if len(articles) == 0 else articles
    return render_template("mood.html", articles=articles, notify=notify,
                           pages=(all_pages, page), user=g.user, form=form)

@app.route("/dream")
@app.route("/dream/<int:page>")
def dream(page=1):
    form = LoginForm()
    page = (int)(request.args.get("page", 1))
    notify = WebsiteConfig.query.filter_by(items="dream-notify").first()
    articles = Article.query.filter_by(type = "梦记",condition=2).order_by(-Article.timestamp).paginate(page, POSTS_PER_PAGE, False).items
    all_pages = (int)(math.ceil(Article.query.filter_by(type = "梦记").count() * 1.0 / POSTS_PER_PAGE))
    articles = "" if len(articles) == 0 else articles
    return render_template("dream.html", articles=articles, notify=notify,
                           pages=(all_pages, page), user=g.user,form=form)