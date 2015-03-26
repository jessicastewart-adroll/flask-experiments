#same as 5_3_login

from flask import Flask, render_template, request
from werkzeug import check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import sqlite3

app = Flask(__name__)
serializer = URLSafeTimedSerializer('top_secret')

@app.route('/tokening', methods=['GET','POST'])
def request_tokening():
	#makes all inputs bytestrings on the way in for consistency (come in as Unicode)
	if request.method == 'POST':
		un = str(request.form['username'])
		pw = str(request.form['password'])
		conn = sqlite3.connect('security.db')
		cur = conn.cursor()
		hashed = str(cur.execute("SELECT password FROM users WHERE username=?", (un,)).fetchone()[0])
		#note: that SQLite requires all Python variables subbed into SQL statements as tuples
		if check_password_hash(hashed, pw):
			return URLSafeTimedSerializer('top_secret').dumps([un, pw])
		else:
			return render_template('tokening.html')
	else:
		return render_template('tokening.html')

@app.route('/resource')
def resource():
	if request.args:
		tokening = request.args.get('tokening')
		try: 
			serializer.loads(tokening, max_age=86400)
			return 'DATA!'
		except SignatureExpired:
			return "Token expired"
		except BadSignature:
			return "Incorrect token"
	else:
		return render_template('tokening.html')

if __name__ == '__main__':
	app.run(debug=True)
