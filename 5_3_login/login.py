#user auth that layers on token auth for a resource page 
#uses the itsdangerous module to generate and verify the token (token has 'timed' features so I set it to expire after a day)
#note: token does not need to be stored server-side
	#rather than being random characters, token encrypts username/password
	#token is decrypted through 'loading'

#unpack user info by 'loading' the token

from flask import Flask, render_template, request
from werkzeug import check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import sqlite3

app = Flask(__name__)
serializer = URLSafeTimedSerializer('top_secret')

@app.route('/token', methods=['GET','POST'])
def request_token():
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
			return render_template('token.html')
	else:
		return render_template('token.html')


@app.route('/resource')
def resource():
	if request.args:
		token = request.args.get('token')
		try: 
			serializer.loads(token, max_age=86400)
			return 'DATA!'
		except SignatureExpired:
			return "Token expired"
		except BadSignature:
			return "Incorrect token"
	else:
		return render_template('token.html')


if __name__ == '__main__':
	app.run(debug=True)
