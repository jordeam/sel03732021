from flask import Blueprint, render_template, Response
from flask_login import login_required, current_user
from . import db
from . import camera_pi
from gpiozero import LED

led = LED(26)
main = Blueprint('main', __name__)


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@main.route('/home')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera_pi.Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@main.route('/abrir', methods=['POST'])
def abrir():
    led.on()
    return render_template('profile.html', name=current_user.name)

@main.route('/fechar', methods=['POST'])
def fechar():
    led.off()
    return render_template('profile.html', name=current_user.name)
