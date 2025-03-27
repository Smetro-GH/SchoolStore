from flask import Blueprint, render_template
from .models import Product

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return '<h1>Test</h1>'

@views.route('/perfil')
def profile():
    return '<h1>Profile</h1>'

@views.route('/tienda')
def buy():
    products = Product.query.all()
    return render_template("Tienda.html", products=products)

@views.route('/carrito')
def cart():
    return '<h1>Cart</h1>'