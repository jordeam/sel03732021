from flask import Blueprint, render_template, Response
from flask_login import login_required, current_user
from . import db
from . import camera_pi
from gpiozero import LED

led = LED(26)
main = Blueprint('main', __name__)

def gen(camera):
    # Função de gerador de streaming de vídeo
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Cria a rota para página de home
@main.route('/home')
def index():
    return render_template('index.html')

# Cria a rota para página de perfil
@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/video_feed')
def video_feed():
    # Rota de streaming de vídeo.
    return Response(gen(camera_pi.Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Cria a rota para o botão de abrir a fechadura
@main.route('/abrir', methods=['POST'])
def abrir():
    led.on()
    return render_template('profile.html', name=current_user.name)

# Cria a rota para o botão de fechar a fechadura
@main.route('/fechar', methods=['POST'])
def fechar():
    led.off()
    return render_template('profile.html', name=current_user.name)
