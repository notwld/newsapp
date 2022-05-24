from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager


db = SQLAlchemy()
DB_NAME = "database.db"


def createApp():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "idkifitismeornot111155"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["STATIC_FOLDER"] = "static"
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")
    
    from .models import User,Post,Comments,Likes
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists("website/"+DB_NAME):
        db.create_all(app=app)
        print("DATABASE CREATED OWO")