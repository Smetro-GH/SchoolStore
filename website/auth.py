from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.profile'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username') or ""
        password = request.form.get('password') or ""
        password2 = request.form.get('password2') or ""

        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Correo electronico debe ser mayor a 4 caracteres', category='error')
        elif len(username) < 2:
            flash('Nombre de usuario debe ser mayor a 2 caracteres', category='error')
        elif len(password) < 6:
            flash('La contraseña debe ser mayor a 6 caracteres', category='error')
        elif password != password2:
            flash('Las contraseñas no coinciden', category='error')
        else:

            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password, method='pbkdf2:sha256')
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Cuenta creada', category='success')
            return redirect(url_for('views.store'))

    return render_template("signup.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))