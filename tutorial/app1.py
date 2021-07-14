#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 13:59:55 2021

@author: jrm
"""

from flask import Flask, render_template

devices_all = [
    {
     'title': 'Device 1',
     'owner': 'Me',
     'content': 'Contents of device 1'
    },
    {
     'title': 'Device 3',
     'owner': 'Someone',
     'content': 'Contents of device 3'
    },
    {
     'title': 'Devices 2',
     'content': 'Contents of device 2'
    },
    ]

app = Flask(__name__)

@app.route('/')
def index():
    return '''
<h1> Hello there!!! </h1>
<p> Another line </p>
<p> <a href="/devices"> Acesse Devices Aqui</a></p>
'''

# Uses a simple template, with no variable content
@app.route('/device')
def device():
    return render_template('device.html')

@app.route('/main/<string:s>')
def main(s):
    return render_template('index.html', s=s)

@app.route('/devices')
def posts():
    return render_template('devices_old.html', devices=devices_all)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
