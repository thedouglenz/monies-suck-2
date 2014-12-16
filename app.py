from __future__ import print_function
import os
from flask import Flask, jsonify, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from flask.ext.bcrypt import Bcrypt
from marshmallow import Serializer

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

bcrpyt = Bcrypt(app)
app.secret_key = "\xcf\x87\xb9_~\xf9t\xb3\x1es\x87\\\xd5\x16FJ\xb7\xc3^mD'IZ"
login_manager = LoginManager(app)

@app.route('/')
def index():
	return render_template('home.html')

if __name__ == '__main__':
    print('Port: ' + os.environ['PORT'])
    app.run(debug=True, host='0.0.0.0')
