from flask import Flask, render_template, redirect, url_for

flask_text_app = Flask(__name__)

@flask_text_app.route('/')
def index():
	return "Welcome to the Flask text portfolio. Append '/hyperlink' to URL above"

@flask_text_app.route('/hyperlink')
def hyperlink_demo():
	return render_template('hyperlink_demo.html')

@flask_text_app.route('/url_for')
def url_for_demo():
	return render_template('url_for_demo.html')

@flask_text_app.route('/css')
def css_demo():
	return render_template('css_demo.html')

@flask_text_app.route('/links')
def links_demo():
	return render_template('links_demo.html')

def not_decorator():
	return "Successfully added a 'view' by creating a view function and then calling the function to add a rule for this view function directly on the Flask object rather than through the route decorator."

flask_text_app.add_url_rule('/no_decorator', 'not_decorator', not_decorator)

@flask_text_app.route('/redirecting')
def redirect_demo():
	return redirect(url_for('index'))

if __name__ == '__main__':
	flask_text_app.run(debug=True)