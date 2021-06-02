#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 13:59:55 2021

@author: jrm
"""

from flask import Flask


app = Flask('__name__')

@app.route('/')
def index():
    return 'Hello there'

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
