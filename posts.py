from flask import Blueprint, render_template, request, redirect, url_for
from application import app, db
import os
from flask.helpers import flash
import json
from flask_login import current_user

from models import Post, Tag, User, Comment
from flask_security import login_required
from werkzeug.utils import secure_filename
from services import EmodjiService

posts = Blueprint("posts",
                  __name__,
                  template_folder="templates")


@posts.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form["post_title"]
        tags = request.form["post_tags"]
        url = request.form["post_exturl"]
        text = request.form["post_text"]
        image = request.files['post_image']
        if title and text:
            text = EmodjiService.emodjis_to_text(text)
            post = Post(title=title, text=text, author_id = current_user.id)
            db.session.add(post)
            db.session.commit()
            if tags:
                tags = tags.split(" ")
                for tag in tags:
                    current_tag = Tag.query.filter(Tag.name == tag).first()
                    if not current_tag:
                        current_tag = Tag(name=tag)
                    post.tags.append(current_tag)
            if url:
                post.external_url = url
            if image:
                filename = secure_filename(image.filename)
                fname =  "posts_images/" + str(post.id) + "." + filename.split(".")[-1]
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], fname).replace("\\", "/"))
                post.picture_src = fname
            else:
                post.picture_src = "default_image"
            
            db.session.commit()
            return redirect(url_for('posts.post_detail', slug=post.slug))
        else:
            flash("Необхідно вказати назву і текст поста!")
            return redirect(url_for("posts.create"))
    else: 
        return render_template("posts/create_post.html")

@posts.route("/<slug>/edit", methods=["POST", "GET"])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if request.method == "POST":
        title = request.form["post_title"]
        tags = request.form["post_tags"]
        url = request.form["post_exturl"]
        text = request.form["post_text"]
        image = request.files['post_image']
        if title and text:
            text = EmodjiService.emodjis_to_text(text)

            post.title = title
            post.text = text
            db.session.commit()
            if tags:
                post.tags = []
                tags = tags.split(" ")
                for tag in tags:
                    current_tag = Tag.query.filter(Tag.name == tag).first()
                    if not current_tag:
                        current_tag = Tag(name=tag)
                    
                    post.tags.append(current_tag)
            if url:
                post.external_url = url
            if image:
                filename = secure_filename(image.filename)
                fname =  "posts_images/" + str(post.id) + "." + filename.split(".")[-1]
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], fname).replace("\\", "/"))
                post.picture_src = fname
            db.session.commit()
            return redirect(url_for('posts.post_detail', slug=post.slug))
        else:
            flash("Необхідно вказати назву і текст поста!")
            return redirect(url_for("posts.edit"))
    else: 
        text = post.text

        text = EmodjiService.text_to_emodjis(text)

        tags = [p.name for p in post.tags]
        tags = " ".join(tags)
        print(tags)
        return render_template("posts/edit_post.html", post=post, text=text, tags=tags)

@posts.route("/")
def index():
    page = request.args.get("page")
    page = int(page) if page and page.isdigit() else 1

    q = request.args.get("q")
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.text.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())
    
    
    pages = posts.paginate(page=page, per_page=5)

    return render_template("posts/index.html", pages=pages)


@posts.route('/<slug>', methods=["GET", "POST"])
def post_detail(slug):
    if request.method == "POST":
        if "add_comment" in request.form:
            comment = request.form["new_comment"]
            if comment:
                post = Post.query.filter(Post.slug == slug).first()
                comm = Comment(text=comment, author_id = current_user.id, post_id=post.id)
                db.session.add(comm)
                db.session.commit()
                date = str(comm.created)
                return json.dumps({'comment': comment, "picture_src": url_for('static',filename=comm.author.picture_src), "name":comm.author.nickname, "date":date})
        if "hit_like" in request.form:
            if current_user.is_authenticated:
                post = Post.query.filter(Post.slug == slug).first()
                print(post)
                if current_user in post.users_liked:
                    print("disliked")
                    del post.users_liked[post.users_liked.index(current_user)]
                else:
                    post.users_liked.append(current_user)
                    print("liked")
                db.session.commit()
                return json.dumps({'likes': len(post.users_liked), "liked":post in current_user.liked_posts})
            else:
                flash("Для початку необхідно увійти!")
                return json.dumps({'redirect': url_for("users.login")})

        if "delete_post" in request.form:
            post = Post.query.filter(Post.slug == slug)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], post.first().picture_src)
            if os.path.exists(filename):
                os.remove(filename)
            post.delete()
            db.session.commit()
            flash("Пост було успішно видалено")
            return redirect(url_for("posts.index"))
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags
    author = User.query.filter(User.id == post.author_id).first()
    text = post.text

    text = EmodjiService.text_to_emodjis(text)

    import requests
    try:
        r = requests.post("https://api.peekalink.io/", headers={"X-API-Key": "1b36dc65-d0b7-4813-9a91-8db371193721"}, data={"link": post.external_url})
    except:
        ext = dict()
        ext["title"] = "Це посилання недоступне"
        ext["url"] = "#"
    else:    
        ext = dict()
        try:
            ext["img_url"] = r.json()['image']['url']
        except:
            try:
                ext["img_url"] = r.json()['icon']['url']
            except:
                ext["img_url"] = url_for('static', filename="pictures/404.png")
        try:
            ext["title"] = r.json()['title']
            ext["url"] = r.json()['url']
        except:
            ext["title"] = "Це посилання недоступне"
            ext["url"] = "#"
    isliked = current_user in post.users_liked
    comments = reversed(post.comments)
    return render_template("posts/post_detail.html", post=post, tags=tags, author=author, ext=ext, txt=text, likes=len(post.users_liked), isliked=isliked, comments=comments)
    
@posts.route("/tag/<slug>")
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts = tag.posts.all()
    return render_template("posts/tag_detail.html", tag=tag, posts=posts)

