from blueprints import app
from blueprints import sessionIdGenerator
from flask import render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import string, re
import mysql.connector

#draw the template
# Intialize MySQL
app.secret_key = sessionIdGenerator.randomID()
cnx = mysql.connector.connect(user="tnpham", password="SFU_cmpt474_P", host="walkingbus1.c11ymny8q9ji.us-east-1.rds.amazonaws.com", port=3306, database='walkingbus1')

@app.route("/")
def direct():
	return redirect(url_for('home'))

#cannot use cnx.close()
#need home html layout
@app.route('/home')
def home():
	if 'logged_in' in session:
		return render_template('home.html', username = session['email'])
	return redirect(url_for('login'))

#Register a new account
@app.route('/login', methods=['GET', 'POST'])
def login():
	output = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		email = request.form['email']
		password = str(request.form['password'])
		# fetch info from database
		cnx.ping(True)
		cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT ID, Email from Users WHERE Email = %s AND Pwd = %s', (email, password))
		account = cursor.fetchone()
		cursor.close()


		if account:
			(userId, email) = account
			session['logged_in'] = True
			session['id'] = userId
			session['email'] = email

			flash('Logged in successfully')
			return redirect(url_for('home'))
		else:
			output = 'Invalid User Credentials'

	return render_template('login.html', msg=output)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Logged out successfully')
	return redirect(url_for('login'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
	output = ''
	#Check if user submits form
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
		username = request.form['username']
		password = str(request.form['password'])
		email = request.form['email']

		cnx.ping(True)
		cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM Users WHERE Email = %s', [email])
		account = cursor.fetchone()
		cursor.close()
		#check if email/account exist already exists
		if account:
			output = 'Account Already Exists'
		#check for valid email
		elif not ifValidEmail(email):
			output = 'Invalid Email Address'
		#check for valid username entry
		elif not ifValidUserName(username):
			output = 'Invalid Username (Must contain letters and numbers only!)'
		elif (len(password) < 5):
			output = 'Password must contain atleast 5 characters'
		elif not username or not password or not email:
			output = 'Please fill out the form!'
		else:
			#Create new Account
			cnx.ping(True)
			cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('INSERT INTO Users (Username, Pwd, Email, UserTypeID) VALUES (%s, %s, %s, 2)', [username, password, email])
			cnx.commit()
			cursor.close()
			output = 'You have successfully registered!'

			return redirect(url_for('login'))

	#Check if field is empty
	elif request.method == 'POST':
		output = 'Please fill the form to complete registration'


	return render_template('register.html', msg = output)


@app.route('/profile')
def profile():
	if session['logged_in'] == True:
		cnx.ping(True)
		cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM Users WHERE Id = %s', [session['id']])
		account = cursor.fetchone()
		cursor.close()
		return render_template('profile.html', account=account)

	return redirect(url_for('login'))
#	if 
def cleanup():
	cnx.commit()
	cnx.close()

#function to check if Username is valid
def ifValidUserName(username = ''):
	if not username:
		return 0
	else:
		if re.match("[A-Za-z0-9]+$", username):
			return True
		else:
			return False


def ifValidEmail(email = ''):
	if not email:
		return 0
	else:
		if re.match('[^@]+@[^@]+\.[^@]+', email):
			return True
		else:
			return False
