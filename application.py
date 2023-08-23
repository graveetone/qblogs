from flask import Flask
from flask_security.datastore import UserDatastore
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, current

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_security import SQLAlchemyUserDatastore

from flask import url_for, redirect, request

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
from models import *
from flask_security import current_user


from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


