from flask import Blueprint, render_template
from .models import Product

admin = Blueprint('admin', __name__)

@admin.route('/Productos')
def products():
    products = Product.query.all()
    return render_template("Productos.html", products=products)

@admin.route('/ordenes')
def orders():
    return '<h1>Orders</h1>'