from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        Username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Correo electronico debe ser mayor a 4 caracteres', category='error')
        elif len(Username) < 2:
            flash('Nombre de usuario debe ser mayor a 2 caracteres', category='error')
        elif len(password) < 6:
            flash('La contraseña debe ser mayor a 6 caracteres', category='error')
        elif password != password2:
            flash('Las contraseñas no coinciden', category='error')
        else:
            flash('Cuenta creada', category='success')

    return render_template("signup.html")

@auth.route('/logout')
def logout():
    return '<p>Logout</p>'