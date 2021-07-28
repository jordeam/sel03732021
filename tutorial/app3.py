#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 13:59:55 2021

@author: jrm
"""

from flask import Flask, render_template
from datetime import datetime

import sqlite3

app = Flask('__name__')

@app.route('/')
def index():
    return 'Hello there'

# Uses a simple static template
@app.route('/device')
def device():
    return render_template('device.html')

@app.route('/main')
def main():
    return render_template('index.html')

@app.route('/devices')
def devices():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    rows = cur.execute('SELECT d.id,d.name,d.value,date(date_create),time(date_create),u.name FROM devices as d,users as u WHERE u.id = owner AND u.id = 1')
    return render_template('devices.html', devices=rows)

@app.route('/list-data')
def list_data():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    rows = cur.execute('SELECT id,ident,dado FROM dados')
    return render_template('list-dados.html', dados=rows)

@app.route('/data/<ids>/<dado>')
def data(ids, dado):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute('INSERT INTO dados (ident,dado,insert_date) values (?,?,julianday(\'now\',\'localtime\'))', (ids,dado))
    # cur.execute('INSERT INTO dados (ident,dado) values (' + sqlite3.quote(ids) + ',' + sqlite3.quote(dado) +')')
    con.commit()
    con.close()
    return render_template('data.html', data = ids + ' enviou: ' + dado)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
