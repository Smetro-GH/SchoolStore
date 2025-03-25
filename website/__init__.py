from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db
from .views import views
from .auth import auth

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'

    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

    with app.app_context():
        db.create_all()

    return app