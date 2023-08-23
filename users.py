import os
from flask import Blueprint, render_template, request, redirect, url_for
from flask.helpers import flash
from flask_security.utils import logout_user
from models import Post, User
from application import app, db
from flask_security import login_required
from werkzeug.utils import secure_filename
import bcrypt
from flask_login import login_user, current_user, logout_user

users = Blueprint("users",
                  __name__,
                  template_folder="templates")

@login_required
@users.route("/myposts")
def my_posts():
    page = request.args.get("page", type=int, default=1)

    q = request.args.get("q")
    if q:
        posts = Post.query.filter(Post.author_id == current_user.id and (Post.title.contains(q) | Post.text.contains(q)))
    else:
        posts = Post.query.filter(Post.author_id == current_user.id).order_by(Post.created.desc())
    
    pages = posts.paginate(page=page, per_page=5)
    return render_template("posts/index.html", pages=pages)

@login_required
@users.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("users.login"))

@users.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]
        user = User.query.filter(User.nickname == nickname).first()
        if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            print("Logged in!")
            login_user(user)
            return redirect(url_for("users.main", id=user.id))
        else:
            flash("Користувача з такими даними не знайдено!")
            return redirect(url_for("users.login"))
    else:
        return render_template("users/login_user.html")


@users.route("/<id>", methods=["GET", "POST"])
@login_required
def main(id):
    user = User.query.filter(User.id == id).first_or_404()
    if request.method == "POST":
        if "delete_user" in request.form:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], user.picture_src)
            if os.path.exists(filename):
                os.remove(filename)
            user = User.query.filter(User.id == id).delete()
            db.session.commit()
            logout_user()
            return redirect(url_for("users.login"))
        else:
            user_photo = request.files['new_uimage']
            filename = secure_filename(user_photo.filename)
            fname =  "users_images/" + str(id) + "." + filename.split(".")[-1]
            if user_photo:
                user_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], fname).replace("\\", "/"))
                user.picture_src = fname
                flash("Зображення успішно змінено!")
            new_nickname = request.form["nickname"]
            if User.query.filter(User.nickname == new_nickname).first():
                flash("Цей нікнейм уже зайнятий!")
            else:
                if new_nickname:
                    user.nickname = new_nickname
                    flash("Нікнейм успішно змінено!")
            new_password = request.form["password"]
            if new_password:
                hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                user.password =  hashed
                flash("Пароль успішно змінено!")
        db.session.commit()
        return render_template("users/user_main.html", user=user)
    db.session.commit()
    return render_template("users/user_main.html", user=user)

@users.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        let_access = True
        user = User()
        nickname = request.form["nickname"]
        password = request.form["password"]
        pswrd = None
        if not nickname:
            flash("Оберіть свій нікнейм!")
            let_access = False
        elif User.query.filter(User.nickname == nickname).first():
            flash("Цей нікнейм уже зайнятий!")
            let_access = False 
        else:
            user.nickname = nickname
        if not password:
            flash("Потрібно обрати пароль!")
            let_access = False
        else:
            pswrd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            user.password = pswrd 
        picture_src = 'users_images/default.png'
        user.picture_src = picture_src
        if let_access:
            db.session.add(user)
            db.session.commit()
        else:
            return render_template("users/register.html")
        user = User.query.filter(User.nickname == nickname).first()
        user_photo = request.files['new_uimage']
        if user_photo:
            filename = secure_filename(user_photo.filename)
            fname =  "users_images/" + str(user.id) + "." + filename.split(".")[-1]
            user_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], fname).replace("\\", "/"))
            user.picture_src = fname
            db.session.commit()
        if let_access:
            return redirect(url_for("users.login"))
        else:
            return render_template("users/register.html")
            
    else:
        
        return render_template("users/register.html")
