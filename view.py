from application import app
from flask import render_template, redirect, url_for

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/")
def main_page():
    return redirect(url_for("posts.index"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404



        