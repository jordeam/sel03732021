#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 13:59:55 2021

@author: jrm
"""

from flask import Flask, render_template


app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('controller.html')


@app.route('/joystick/<string:s>')
def joystick(s):
    x, y = s.split(',')
    return render_template('index.html', s=s)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)

