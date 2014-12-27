from __future__ import print_function
import os, datetime, calendar
from flask import Flask, jsonify, request, abort, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from flask.ext.bcrypt import Bcrypt
from marshmallow import Serializer

import random, json, decimal

from config import TRANSACTIONS_PER_PAGE

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
	name = db.Column(db.String, unique=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	user = db.relationship('User',  backref=db.backref('expense_types',lazy='dynamic'))

	def __init__(self, name, user_id):
		self.name = name
		self.user_id = user_id

	class Serializer(Serializer):
		class Meta:
			fields =("id", "name", "user_id")

class Transaction(db.Model):
	__tablename__ = 'transactions'

	id = db.Column(db.Integer, primary_key=True)
	trans_date = db.Column(db.DateTime(timezone=True), index=True, nullable=False)
	desc = db.Column(db.String, nullable=False)
	amount = db.Column(db.Numeric, nullable=False)
	expense_type_id = db.Column(db.Integer, db.ForeignKey('expense_types.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	user = db.relationship('User',  backref=db.backref('transactions', lazy='dynamic'))
	expense = db.relationship('ExpenseType', backref=db.backref('expense_types', lazy='dynamic'))

	def __init__(self, date, desc, e_type_id, amount, user_id):
		self.trans_date = date
		self.desc = desc
		self.expense_type_id = e_type_id
		self.amount = amount
		self.user_id = user_id

	class Serializer(Serializer):
		class Meta:
			fields = ("id", "trans_date", "desc", "expense_type_id", "amount", "user_id")

# ROUTES

@app.route('/')
def index():
	if current_user.is_authenticated(): # they're already logged in
		return redirect(url_for('dashboard'))
	else: # they're not already logged in
		return render_template('home.html')

@app.route('/create_db')
def create_db():
	db.create_all();
	return "Database generated"

# FUNCS
def random_color():
	# stolen from Dmitry Dubovitsky http://stackoverflow.com/a/14019260/3250878 ; http://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
	r = lambda: random.randint(0,255)
	return ('#%02X%02X%02X' % (r(),r(),r()))

def get_monthly_totals(month_num):
	totals = {}
	expensetypes = current_user.expense_types.order_by(ExpenseType.name).all()
	for e in expensetypes:
		totals[e.name] = db.session.query(db.func.sum(Transaction.amount).label('sum')).filter(Transaction.expense_type_id == e.id, db.func.extract('month', Transaction.trans_date) == month_num).scalar()
	totals = sorted(totals.items(), key=lambda x:x[1], reverse=True)
	return totals

def decimal_default(obj):
	if isinstance(obj, decimal.Decimal):
		return float(obj)
	raise TypeError


@app.route('/dash/<int:page>')
@app.route('/dash/')
@login_required
def dashboard(page=1):
	transactions = current_user.transactions.order_by(Transaction.trans_date.desc()).paginate(page, TRANSACTIONS_PER_PAGE, False)
	expensetypes = current_user.expense_types.order_by(ExpenseType.name).all()

	# this month stuff
	this_month = datetime.datetime.now().month
	month_name = calendar.month_name[this_month]

	totals = get_monthly_totals(this_month)

	return render_template('dashboard.html', expensetypes=expensetypes, transactions=transactions, totals=totals, month_name=month_name)

@app.route('/api/v1/totals/month')
@login_required
def monthly_totals():
	data = []
	tm = get_monthly_totals(datetime.datetime.now().month) # tm is a list of sorted tuples
	for t in tm:
		data.append({
			'value':		t[1],
			'color':		random_color(),
			'highlight':	random_color(),
			'label' :	t[0]
			})
	return json.dumps(data, default=decimal_default)


@app.route('/expensetypes/create')
@login_required
def create_expense_type():
	return render_template('create_expense_type.html')

@app.route('/expensetypes/create', methods=['POST'])
@login_required
def create_expense_type_post():
	new_et = ExpenseType(request.form['name'], current_user.id)
	db.session.add(new_et)
	db.session.commit()
	return redirect(url_for('dashboard'))

@app.route('/expensetypes/<int:expense_type_id>/delete')
@login_required
def delete_expense_type(expense_type_id):
	e = ExpenseType.query.get(expense_type_id)
	if not e.user_id == current_user.id:
		abort(401)
	if e:
		db.session.delete(e)
		db.session.commit()
	return redirect(url_for('dashboard'))

@app.route('/transactions/add')
@login_required
def add_transaction():
	expensetypes = current_user.expense_types.order_by(ExpenseType.name).all()
	return render_template('add_transaction.html', expensetypes=expensetypes)

@app.route('/transactions/add', methods=["POST"])
@login_required
def add_transaction_post():
	t_date = request.form['trans_date']
	desc = request.form['desc']
	e_type_id = request.form['expensetype']
	amount = request.form['amount']
	user_id = current_user.id

	new_transaction = Transaction(t_date, desc, e_type_id, amount, user_id);
	db.session.add(new_transaction)
	db.session.commit()
	return redirect(url_for('dashboard'))

@app.route('/transactions/<int:trans_id>/delete')
@login_required
def delete_transaction(trans_id):
	t = Transaction.query.get(trans_id)
	if not t.user_id == current_user.id:
		abort(401)
	if t:
		db.session.delete(t)
		db.session.commit()
	return redirect(url_for('dashboard'))

@app.route('/transactions/<int:trans_id>/update_exp', methods=['POST'])
def update_trans_exp(trans_id):
	t = Transaction.query.get(trans_id)
	if not t.user_id == current_user.id:
		abort(401)
	if t:
		t.expense_type_id = request.form['expense_id']
		db.session.commit()
	return redirect(url_for('dashboard'))

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

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

# Custom error handlers
@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
