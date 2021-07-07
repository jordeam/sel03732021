#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 13:59:55 2021

@author: jrm
"""

from flask import Flask, render_template, url_for, request, jsonify

from flask_socketio import SocketIO, emit, send

app = Flask(__name__, template_folder='templates')
io = SocketIO(app)


@app.route('/')
def index():
    return render_template('controller.html')


@io.on('get_input')
def get_input_handler(msg):
    print(msg)




if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)

