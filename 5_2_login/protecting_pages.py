#password encryption - using hash functions from the werkzeug module 
#login protected pages - added a 'logged in' status to the session (functionally a dictionary that lives on the app)
#logout - redirect URL that pops 'logged in' from the session 

from flask import Flask, render_template, request, redirect, session
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'test'

@app.route('/login', methods = ['GET', 'POST'])
def login_view():
	if request.method == 'POST':
		pwhash = generate_password_hash(request.form['password'])
		pw = open('secret.txt','r').read().strip()
		if request.form['username'] == 'admin' and check_password_hash(pwhash,pw):
			session['status'] = 'logged_in'
			return redirect('/mydata')
	return render_template('login.html')

@app.route('/mydata', methods = ['GET', 'POST'])
def user_view():
	if 'logged_in' not in session.values():
		return redirect('/login')
	else:
		return render_template('user.html')

@app.route('/everyones_data', methods = ['GET', 'POST'])
def everyone_view():
	if 'logged_in' not in session.values():
		return redirect('/login')
	else:
		return render_template('everyone.html')

@app.route('/logout')
def logout():
	session.pop('status')
	return redirect('/login')

if __name__ == '__main__':
	app.run(debug=True)

#NOTES
	#secret_key must be set to use the session for storage
	#Chrome browser has logic that overrides the 'autocomplete="off"' attribute on HTML forms so I input the "display:none" attribute as a workaround
	#when checking session status, "if session['status']" throws error if does not contain 'status' so use 'in' syntax
