from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# iniciando o SQLAlchemy para que possamos usá-lo mais tarde em nossos modelos 
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Anni@_1672Mirabiles'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # Uma vez que o user_id é apenas a chave primária de nossa tabela de usuário, use-o na consulta para o usuário 
        return User.query.get(int(user_id))

    # Projeto para rotas de autenticação em nosso aplicativo
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Projeto para partes sem autenticação do aplicativo
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
