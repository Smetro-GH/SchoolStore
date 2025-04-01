from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .models import db, User, Product
from .views import views
from .auth import auth
from .admin import admin
from werkzeug.security import generate_password_hash
import os

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicialización de extensiones
    db.init_app(app)
    
    # Configuración de Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # Registro de blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(admin, url_prefix='/admin/')
    
    # Creación de la base de datos
    with app.app_context():
        db.create_all()
        
        # Crear usuario administrador si no existe
        admin_user = User.query.filter_by(email='admin@schoolstore.com').first()
        if not admin_user:
            admin_user = User(
                email='admin@schoolstore.com',
                username='admin',
                password=generate_password_hash('Anglo123', method='pbkdf2:sha256'),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
        
        # Crear productos base si no existen
        if not Product.query.first():
            productos_base = [
                {
                    'name': 'Hamburguesa Clásica',
                    'description': 'Deliciosa hamburguesa con carne 100% de res, lechuga, tomate y salsa especial',
                    'price': 45.00,
                    'quantity': 50,
                    'category': 'alimento'
                },
                {
                    'name': 'Pizza Margherita',
                    'description': 'Pizza tradicional con salsa de tomate, mozzarella y albahaca fresca',
                    'price': 65.00,
                    'quantity': 30,
                    'category': 'alimento'
                },
                {
                    'name': 'Ensalada César',
                    'description': 'Lechuga romana, crutones, parmesano y aderezo césar',
                    'price': 35.00,
                    'quantity': 40,
                    'category': 'alimento'
                },
                {
                    'name': 'Sándwich Club',
                    'description': 'Pollo, tocino, lechuga, tomate y mayonesa en pan tostado',
                    'price': 40.00,
                    'quantity': 45,
                    'category': 'alimento'
                },
                {
                    'name': 'Pasta Alfredo',
                    'description': 'Fetuccini en salsa cremosa con queso parmesano',
                    'price': 55.00,
                    'quantity': 35,
                    'category': 'alimento'
                },
                {
                    'name': 'Coca-Cola',
                    'description': 'Refresco Coca-Cola 600ml',
                    'price': 15.00,
                    'quantity': 100,
                    'category': 'bebida'
                },
                {
                    'name': 'Agua Mineral',
                    'description': 'Agua mineral natural 500ml',
                    'price': 10.00,
                    'quantity': 150,
                    'category': 'bebida'
                },
                {
                    'name': 'Jugo de Naranja',
                    'description': 'Jugo de naranja natural 500ml',
                    'price': 20.00,
                    'quantity': 80,
                    'category': 'bebida'
                },
                {
                    'name': 'Café Americano',
                    'description': 'Café americano caliente 300ml',
                    'price': 25.00,
                    'quantity': 60,
                    'category': 'bebida'
                },
                {
                    'name': 'Té Helado',
                    'description': 'Té helado de limón 500ml',
                    'price': 18.00,
                    'quantity': 70,
                    'category': 'bebida'
                }
            ]
            
            for producto in productos_base:
                product = Product(**producto)
                db.session.add(product)
            
            db.session.commit()
    
    return app