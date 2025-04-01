from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import Product, Order, db
from functools import wraps
import os
from werkzeug.utils import secure_filename

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acceso no autorizado.', category='error')
            return redirect(url_for('views.home'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    products = Product.query.all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin/dashboard.html", products=products, orders=orders)

@admin.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        quantity = int(request.form.get('quantity', 0))
        category = request.form.get('category')
        image = request.files.get('image')

        if not name or price <= 0 or quantity < 0 or not category:
            flash('Por favor complete todos los campos correctamente.', category='error')
            return redirect(url_for('admin.add_product'))

        image_url = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            # Asegurarse de que el directorio existe
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            # Guardar la imagen
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)
            image_url = f'/static/uploads/{filename}'

        product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category=category,
            image_url=image_url
        )

        db.session.add(product)
        db.session.commit()
        flash('Producto agregado exitosamente.', category='success')
        return redirect(url_for('admin.dashboard'))

    return render_template("admin/product_form.html")

@admin.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        quantity = int(request.form.get('quantity', 0))
        category = request.form.get('category')
        image = request.files.get('image')

        if not name or price <= 0 or quantity < 0 or not category:
            flash('Por favor complete todos los campos correctamente.', category='error')
            return redirect(url_for('admin.edit_product', product_id=product_id))

        image_url = product.image_url
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            # Asegurarse de que el directorio existe
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            # Guardar la imagen
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)
            image_url = f'/static/uploads/{filename}'
            # Eliminar la imagen anterior si existe
            if product.image_url and product.image_url.startswith('/static/uploads/'):
                old_image_path = os.path.join(current_app.root_path, product.image_url.lstrip('/'))
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

        product.name = name
        product.description = description
        product.price = price
        product.quantity = quantity
        product.category = category
        product.image_url = image_url

        db.session.commit()
        flash('Producto actualizado exitosamente.', category='success')
        return redirect(url_for('admin.dashboard'))

    return render_template("admin/product_form.html", product=product)

@admin.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Eliminar la imagen si existe
    if product.image_url and product.image_url.startswith('/static/uploads/'):
        image_path = os.path.join(current_app.root_path, product.image_url.lstrip('/'))
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado exitosamente.', category='success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/orders')
@login_required
@admin_required
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin/orders.html", orders=orders)

@admin.route('/orders/<int:order_id>/update-status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'completed', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash('Estado de la orden actualizado exitosamente.', category='success')
    else:
        flash('Estado de orden inválido.', category='error')
    
    return redirect(url_for('admin.orders'))