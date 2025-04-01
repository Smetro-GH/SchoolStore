from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from .models import Product, Order, OrderItem, Payment, db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/store')
def store():
    products = Product.query.all()
    return render_template("store.html", products=products)

@views.route('/cart')
@login_required
def cart():
    cart_items = session.get('cart', [])
    total = 0
    items = []
    
    for item in cart_items:
        product = Product.query.get(item['product_id'])
        if product:
            items.append({
                'product': product,
                'quantity': item['quantity'],
                'subtotal': product.price * item['quantity']
            })
            total += product.price * item['quantity']
    
    return render_template("cart.html", items=items, total=total)

@views.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    product = Product.query.get_or_404(product_id)
    
    if quantity > product.quantity:
        flash('No hay suficiente stock disponible.', category='error')
        return redirect(url_for('views.store'))
    
    cart = session.get('cart', [])
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            break
    else:
        cart.append({
            'product_id': product_id,
            'quantity': quantity
        })
    
    session['cart'] = cart
    flash('Producto agregado al carrito.', category='success')
    return redirect(url_for('views.store'))

@views.route('/remove-from-cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['product_id'] != product_id]
    session['cart'] = cart
    flash('Producto removido del carrito.', category='success')
    return redirect(url_for('views.cart'))

@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        if not payment_method:
            flash('Por favor seleccione un método de pago.', category='error')
            return redirect(url_for('views.checkout'))
        
        cart_items = session.get('cart', [])
        if not cart_items:
            flash('El carrito está vacío.', category='error')
            return redirect(url_for('views.cart'))
        
        total = 0
        order_items = []
        
        for item in cart_items:
            product = Product.query.get(item['product_id'])
            if product and product.quantity >= item['quantity']:
                total += product.price * item['quantity']
                order_items.append({
                    'product': product,
                    'quantity': item['quantity']
                })
                product.quantity -= item['quantity']
            else:
                flash('No hay suficiente stock disponible.', category='error')
                return redirect(url_for('views.cart'))
        
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            payment_method=payment_method
        )
        db.session.add(order)
        
        for item in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price_at_time=item['product'].price
            )
            db.session.add(order_item)
        
        payment = Payment(
            order_id=order.id,
            amount=total,
            payment_method=payment_method,
            status='completed'
        )
        db.session.add(payment)
        
        db.session.commit()
        session['cart'] = []
        
        flash('¡Pago exitoso! Puede recoger su pedido en la tienda.', category='success')
        return redirect(url_for('views.store'))
    
    cart_items = session.get('cart', [])
    total = 0
    items = []
    
    for item in cart_items:
        product = Product.query.get(item['product_id'])
        if product:
            items.append({
                'product': product,
                'quantity': item['quantity'],
                'subtotal': product.price * item['quantity']
            })
            total += product.price * item['quantity']
    
    return render_template("checkout.html", items=items, total=total)

@views.route('/profile')
@login_required
def profile():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template("profile.html", orders=orders)