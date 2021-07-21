from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from flask_socketio import SocketIO, emit, send

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/controller')
@login_required
def profile():
    return render_template('controller.html', name=current_user.name)


