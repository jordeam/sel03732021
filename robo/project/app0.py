#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, render_template, url_for, request, jsonify
import logging
from flask_socketio import SocketIO, emit, send
from engineio.payload import Payload


Payload.max_decode_packets = 500

app = Flask(__name__, template_folder='templates')
sio = SocketIO(app)
#sio = SocketIO(app, async_mode='gevent_uwsgi')
logging.getLogger('werkzeug').setLevel(logging.ERROR)



@app.route('/')
def index():
    return render_template('controller.html')


pos_1_antes = [0,0]
pos_2_antes = [0,0]

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



if __name__ == '__main__':

    app.run('0.0.0.0', 5000, debug=True)

    


