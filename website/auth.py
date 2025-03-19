from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return '<p>Login</p>'

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    return '<p>signup</p>'

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return '<p>Logout</p>'