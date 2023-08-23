from application import app, db
from models import User, Post
import bcrypt

models = [User, Post]

# clear tables
with app.app_context():
    for model in models:
        db.session.query(model).delete()

    user = User(
            nickname='user1',
            picture_src='https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cmFuZG9tJTIwcGVvcGxlfGVufDB8fDB8fHww&w=1000&q=80')

    pswrd = bcrypt.hashpw('pass1234'.encode("utf-8"), bcrypt.gensalt())
    user.password = pswrd 
    user.posts = [
        Post(
            title='Python language is so cool',
            text='Python is hight-level programming language',
            picture_src='https://assets.rbl.ms/33364099/origin.jpg',
            external_url='https://www.python.org/'),
        Post(
            title='Ruby language is also awesome',
            text='Ruby is hight-level object-oriented programming language',
            picture_src='https://media.geeksforgeeks.org/wp-content/cdn-uploads/20190902124355/ruby-programming-language.png',
            external_url='https://www.ruby-lang.org/en/')
    ]

    db.session.add(user)
    db.session.commit()