from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')
    
@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # checando se o usuário existe
    # comparando a senha com a db
    if not user or not check_password_hash(user.password, password):
        flash('Verfique seu email e senha e tente novamente')
        return redirect(('app-08/login')) # se o usuário não exixtis ou a senha estiver errada, reload na page.

   
    login_user(user, remember=remember)
    return redirect('app-08/profile')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    #confirma = request.form.get('confirma')

    user = User.query.filter_by(email=email).first() 

    if user: 
	    flash('E-mail já cadastrado, tente novamente!')
	    return redirect('app-08/signup')

 
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
   

    db.session.add(new_user)
    db.session.commit()

    return redirect('app-08/login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('app-08/home')



