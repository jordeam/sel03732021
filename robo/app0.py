#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, render_template, url_for, request, jsonify
import logging
from flask_socketio import SocketIO, emit, send
from engineio.payload import Payload


Payload.max_decode_packets = 100

app = Flask(__name__, template_folder='templates')
sio = SocketIO(app)
#sio = SocketIO(app, async_mode='gevent_uwsgi')
logging.getLogger('werkzeug').setLevel(logging.ERROR)



@app.route('/')
def index():
    return render_template('controller.html')



msg_antes = 0

@sio.on('get_input')
def get_input_handler(msg):

    global msg_antes
    if msg_antes != msg:
        print('Coordenadas')
        print(msg)
        msg_antes = msg


        sio.emit('robot_get_input', msg)
        



if __name__ == '__main__':

    app.run('0.0.0.0', 5000, debug=True)

    


