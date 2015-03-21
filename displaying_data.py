import string
from flask import Flask

display_data = Flask(__name__)

@display_data.route('/')
def index():
	return open('test.txt', 'r').read()

@display_data.route('/one')
def one():
	return open('test.txt', 'r').read().split('\n\n')[0]

@display_data.route('/authors')
def authors():
	book_chunks = open('test.txt', 'r').read().split('\n\n')
	return str([i.splitlines()[1].split('AUTHOR: ')[1].translate(None, string.punctuation).lower().replace(' ', '_') for i in book_chunks if i])

@display_data.route('/authors/<author>')
def an_author(author):

	book_chunks = open('test.txt', 'r').read().split('\n\n')
	authors = [i.splitlines()[1].split('AUTHOR: ')[1].translate(None, string.punctuation).lower().replace(' ', '_') for i in book_chunks if i]

	d = {}

	for i, a in enumerate(authors):
		d[a] = book_chunks[i]

	return d[author]

if __name__ == '__main__':
	display_data.run(debug=True)
