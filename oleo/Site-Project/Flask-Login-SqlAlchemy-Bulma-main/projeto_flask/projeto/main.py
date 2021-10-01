from re import DEBUG
from flask import Blueprint, render_template, request, Flask
import flask
from flask_login import login_required, current_user
import json
import sqlite3
from datetime import datetime
from .import data

#incialização de aplicação FLASK
main = Blueprint('main', __name__)


#POSTAGEM JSON
@main.route('/postjson', methods = ['POST'])
def postjson():
        print(flask.request.get_data())
        data1 = flask.request.get_data()
        j = json.loads(data1)
        ids = str(j['sensor'])
        dado = str(j['Nivel'])
        con = sqlite3.connect('data.sqlite')
        cur = con.cursor()
        if ids == '20w50':
            cur.execute('UPDATE dados SET value = ? WHERE sensor = ?',(dado,ids))
        else:
            cur.execute('INSERT INTO dados (sensor,value,insertdate) values (?,?,julianday(\'now\',\'localtime\'))', (ids,dado))
        con.commit()
        con.close()
        return j

 #incialização da aplicação FLASK        
if __name__ == '__main__':
        main.run(debug=True)


#redirecionamentos genéricos
@main.route('/')
@main.route('/home')
def index():
    return render_template('index.html')

@main.route('/profile', methods = ['GET', 'POST'])
def profile():
    con = sqlite3.connect('data.sqlite')
    cur = con.cursor()
    rows = cur.execute('SELECT id,sensor,value FROM dados')
    return render_template('profile.html', name=current_user.name, dados=rows)




    
