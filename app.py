from application import app
import view
from users import users
from posts import posts

app.register_blueprint(posts, url_prefix="/blog")
app.register_blueprint(users, url_prefix="/user")

if __name__ == "__main__":
    app.run()
