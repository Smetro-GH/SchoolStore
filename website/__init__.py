from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .models import db
from .views import views
from .auth import auth
from .admin import admin

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'

    db.init_app(app)

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(admin, url_prefix='/admin/')

    with app.app_context():
        db.create_all()

    return app