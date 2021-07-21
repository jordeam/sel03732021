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

    # Verifica se o usuário realmente existe
    # Pega a senha provida pelo usuário, encripta ela pelo 'hash', e compara com o valor em 'hash' do database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect('login') # Se o usuário não existe ou a senha está incorreta, recarrega a página

    # Se a verificação acima é passada, então o usuário existe e colocou a senha correta
    login_user(user, remember=remember)
    return redirect('app-06/profile')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    confirma= request.form.get('confirma')

    user = User.query.filter_by(email=email).first() # Se esta função retorna um usuário, significa que o email ja é cadastrado

    if user: # Se o usuário colocou um email já cadastrado, ele é redirecionado para a página de cadastramento novamente
	    flash('E-mail já cadastrado, tente novamente!')
	    return redirect('signup')

    #if password == confirma:
        # Cria um novo usuário com as credenciais adicionadas
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    #else:
      #  flash('Senhas distintas, tente novamente!')
      #  return redirect(url_for('auth.signup'))

    # Adiciona o novo usuário na database
    db.session.add(new_user)
    db.session.commit()

    return redirect('login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('app-06/home')




