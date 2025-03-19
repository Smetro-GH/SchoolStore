from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return '<h1>Test</h1>'

@views.route('/perfil')
def profile():
    return '<h1>Profile</h1>'

@views.route('/tienda')
def buy():
    return render_template("Tienda.html")

@views.route('/carrito')
def cart():
    return '<h1>Cart</h1>'