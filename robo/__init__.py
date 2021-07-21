from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO, emit, send
from engineio.payload import Payload
import logging

# seta payload maximo
Payload.max_decode_packets = 500

# suprime mensagem de log
logging.getLogger('werkzeug').setLevel(logging.ERROR)


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
pos_1_antes = [0,0]
pos_2_antes = [0,0]

def create_app():
    app = Flask(__name__)
    sio = SocketIO(app)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)



    @sio.on('get_input')
    def get_input_handler(data):

        global pos_1_antes, pos_2_antes
        pos_1 = [int(data['X1']),int(data['Y1'])]
        pos_2 = [int(data['X2']),int(data['Y2'])]
        # roda apenas se a mensagem foi alterada 
        if pos_1_antes != pos_1:
            print('Enviando coordenadas robo1:\n',pos_1)
            pos_1_antes = pos_1
            # emite o input para clients conectados
            sio.emit('robot1_get_input', pos_1)
        if pos_2_antes != pos_2:
            print('Enviando coordenadas robo2:\n',pos_2)
            pos_2_antes = pos_2
            # emite o input para clients conectados
            sio.emit('robot2_get_input', pos_2)      



    return app