from application import app
import view
from application import db

from blueprint import posts, users

app.register_blueprint(posts , url_prefix="/blog")
app.register_blueprint(users, url_prefix="/user")

if __name__ == "__main__":
    app.run()
