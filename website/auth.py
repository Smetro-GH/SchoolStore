from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re


auth = Blueprint('auth', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('¡Inicio de sesión exitoso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.store'))
            else:
                flash('Contraseña incorrecta, intente de nuevo.', category='error')
        else:
            flash('El usuario no existe.', category='error')

    return render_template("login.html")

@auth.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if password == 'Anglo123':  # Contraseña predeterminada para administrador
            user = User.query.filter_by(username=username).first()
            if user:
                user.is_admin = True
                db.session.commit()
                login_user(user, remember=True)
                flash('¡Inicio de sesión como administrador exitoso!', category='success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('El usuario no existe.', category='error')
        else:
            flash('Contraseña de administrador incorrecta.', category='error')

    return render_template("admin_login.html")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validaciones
        if not validate_email(email):
            flash('Correo electrónico inválido.', category='error')
            return render_template("signup.html")

        if len(username) < 2:
            flash('El nombre de usuario debe tener al menos 2 caracteres.', category='error')
            return render_template("signup.html")

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', category='error')
            return render_template("signup.html")

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', category='error')
            return render_template("signup.html")

        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('El correo electrónico ya está registrado.', category='error')
            return render_template("signup.html")

        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash('El nombre de usuario ya está en uso.', category='error')
            return render_template("signup.html")

        new_user = User(
            email=email,
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )

        db.session.add(new_user)
        db.session.commit()
        flash('¡Cuenta creada exitosamente! Por favor, inicie sesión.', category='success')
        return redirect(url_for('auth.login'))

    return render_template("signup.html")

@auth.route('/logout')
@login_required
def logout():
    if current_user.is_admin:
        current_user.is_admin = False
        db.session.commit()
    logout_user()
    flash('¡Cierre de sesión exitoso!', category='success')
    return redirect(url_for('views.home'))
