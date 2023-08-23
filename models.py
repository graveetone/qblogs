from enum import unique
from sqlalchemy.orm import backref
from application import db
from datetime import date, datetime
import re
from flask_login import UserMixin
from flask_login import current_user

def slugify(string):
    pattern = r"[^\w+]"
    another_pattern = r"-+"
    return re.sub(another_pattern, "-", re.sub(pattern, "-", string))


post_tags = db.Table("post_tags", db.Column("post_id", db.Integer, db.ForeignKey('post.id', ondelete="SET NULL")), db.Column("tag_id", db.Integer, db.ForeignKey("tag.id", ondelete="SET NULL")))
post_likes = db.Table("post_likes", db.Column("post_id", db.Integer, db.ForeignKey('post.id', ondelete="SET NULL")), db.Column("user_id", db.Integer, db.ForeignKey("user.id", ondelete="SET NULL")))
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)  # unique url
    text = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    picture_src = db.Column(db.String(250)) 
    external_url = db.Column(db.String(250))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    comments = db.relationship("Comment", backref="post")

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    tags = db.relationship("Tag", secondary=post_tags, backref=db.backref('posts', lazy="dynamic"))
    users_liked = db.relationship("User", secondary=post_likes, backref=db.backref('liked_posts', lazy="dynamic"))
    def generate_slug(self):
        import datetime
        x = datetime.datetime.now()
        components = list(map(lambda c: str(c), [x.day, x.month, x.year, x.hour, x.minute, x.second]))
        slug_date = "".join(components)
        if self.title:
            self.slug = slugify(self.title+' '+slug_date)

    
    def __repr__(self):
        return f"<Post id: {self.id} title: {self.title}>"
        

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)
    
    def __repr__(self):
        return self.name
    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    nickname = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    posts = db.relationship("Post", backref="author")
    comments = db.relationship("Comment", backref="author")
    picture_src = db.Column(db.String(255))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"))
    created = db.Column(db.DateTime, default=datetime.now)