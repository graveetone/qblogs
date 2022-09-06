import datetime
from flask_migrate import current
from application import app
from flask import render_template
from models import Post, User, Comment, db
from flask import request, redirect, url_for
from flask_login import current_user
import json

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/")
def main_page():
    return redirect(url_for("posts.index"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404



        