# make flask app directory
# make virtualenv, otherwise pip freeze will get all packages in global which will slow down server, venv ensures only needed dependencies added
# activate virtualenv, add all needed packages 
# make requirements.txt, put dependencies in requirements file
# make flask app file (app.py)
# make Procfile
# git init, create .gitignore file and add virtualenv file, add commit -- creating isolated repo will make commits to heroku easier
# heroku create, rename, push -- creates server that can push to just like git 
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
