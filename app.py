from __future__ import print_function
import os
from flask import Flask, jsonify, request, abort, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from flask.ext.bcrypt import Bcrypt
from marshmallow import Serializer

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
app.secret_key = "\xcf\x87\xb9_~\xf9t\xb3\x1es\x87\\\xd5\x16FJ\xb7\xc3^mD'IZ"
login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

# SCHEMA

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	salary = db.Column(db.Numeric)
	last_active_date = db.Column(db.DateTime(timezone=True), index=True)

	def __init__(self, email, password):
		self.email = email
		self.password = password

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	class Serializer(Serializer):
		class Meta:
			fields = ("id", "email", "salary", "last_active_date")

class ExpenseType(db.Model):
	__tablename__ = 'expense_types'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	user = db.relationship('User', backref=db.backref('expense_types', lazy='dynamic'))

	def __init__(self, name, user_id):
		self.name = name
		self.user_id = user_id

	class Serializer(Serializer):
		class Meta:
			fields =("id", "name", "user_id")

# ROUTES

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/dash')
@login_required
def dashboard():
	return render_template('dashboard.html')

@app.route('/expensetypes/create')
@login_required
def create_expense_type():
	pass

@app.route('/expensetypes/create', methods=['POST'])
@login_required
def create_expense_type_post():
	pass

@app.route('/user/register')
def register_user():
	return render_template('register.html')

@app.route('/user/register', methods=['POST'])
def register_user_post():
	exists = User.query.filter(db.func.lower(User.email) == request.form['email'].lower()).first()
	if exists:
		return "This user already exists"
	hashword = bcrypt.generate_password_hash(request.form['password'])
	new_user = User(request.form['email'], hashword)
	db.session.add(new_user)
	db.session.commit()
	login_user(new_user)
	return redirect(url_for('dashboard'))

@app.route('/login', methods=['POST'])
def login():
	user = User.query.filter(db.func.lower(User.email) == request.form['email'].lower()).first()
	if user and bcrypt.check_password_hash(user.password, request.form['password']):
		login_user(user)
		return redirect(url_for('dashboard'))
	else:
		abort(401)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
