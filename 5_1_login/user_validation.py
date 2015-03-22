from flask import Flask, render_template, request, url_for, redirect

user_reg_app = Flask(__name__)

def login_view_func():
	if request.method == 'POST':
		if request.form['username'] == 'admin' and request.form['password'] == 'secret':
			return inside_view_func()
	
	return render_template('login.html')

def inside_view_func():
	return "You're in!"

login_view_func.methods = ['GET', 'POST']
user_reg_app.add_url_rule('/login_rule', 'login_endpoint', login_view_func)

user_reg_app.add_url_rule('/inside_rule', 'inside_endpoint', inside_view_func)

if __name__ == '__main__':
	user_reg_app.run(debug=True)

#Flask functions:
	#render visual information (which can itself contain Python logic in the HTML via Jinja2)
	#execute python logic that evaluates received information 

#SECURTIY
#user input can be sent with GET but it appears as query string parameters in the url
#this creates the need to use the POST method, which moves the input from the query 
#string to the request.form

#ROUTING
#more complex than expected because some of the routing logic is kept in the HTML

#HTML
#the form attribute listens for the submit button, and then sends input data to a file (here, our login page)
#added logic to the Flask login function to validate form data when it sees 'post'

#werkzeug MultiDict object is how Flask receives post data
	#Python dict to handle request information, extended to accomodate multiple identical keys

#Flask redirect function must be used in order to change both the URL and page data after executing python logic
