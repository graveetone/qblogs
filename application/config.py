class Configuration():
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@localhost/qblogs_db"
    SECRET_KEY = "svSECRET_iat"
    UPLOAD_FOLDER = "static"
    SECURITY_MSG_LOGIN = ("Вам необхідно авторизуватися!", "info")