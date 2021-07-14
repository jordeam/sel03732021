#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, render_template, url_for, request, jsonify
import logging
from flask_socketio import SocketIO, emit, send
from engineio.payload import Payload

Payload.max_decode_packets = 50



app = Flask(__name__, template_folder='templates')
io = SocketIO(app)
#io = SocketIO(app, async_mode='gevent_uwsgi')
logging.getLogger('werkzeug').setLevel(logging.ERROR)

@app.route('/')
def index():
    return render_template('controller.html')


msg_antes = 0

@io.on('get_input')
def get_input_handler(msg):

    global msg_antes
    if msg_antes != msg:
        print('Coordenadas')
        print(msg)

        pos_X = int(msg['X'])
        pos_Y = int(msg['Y'])
        msg_antes = msg
        #print(msg['Dir'])


if __name__ == '__main__':

    app.run('0.0.0.0', 5000, debug=True)
    


