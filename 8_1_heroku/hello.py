# make app directory
# make virtualenv (so pip freeze is contained)
# activate virtualenv
# make app.py
# make requirements.txt
# make Procfile
# git init (so web app is contained), add (not venv), commit
# heroku create, rename, push
# add dyno

# http://test-8-1.herokuapp.com/

import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello wordl"

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))  # port 5000 only works in development, instead get PORT environ var or will return Application Error
	app.run(host='0.0.0.0', port=port) #adding debug=True will put on https
