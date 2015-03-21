#populating Flask views using Sqlite queries

from string import punctuation

from flask import Flask
import sqlite3

trying_sqlite = Flask(__name__)

@trying_sqlite.route('/')
def index():
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute('select * from books')
	return str(c.fetchall())

@trying_sqlite.route('/authors')
def authors():
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute('select author from books')
	authors = c.fetchall()
	return str([str(a[0]).lower().translate(None, punctuation).replace(' ', '_') for a in authors])

@trying_sqlite.route('/authors/<author>')
def author_page(author):
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute('select author from books')
	raw_authors = set(c.fetchall())
	http_raw = [[str(a[0]).lower().translate(None, punctuation).replace(' ', '_'), str(a[0])] for a in raw_authors] 

	d = {}
	for http, raw in http_raw:
		d[http] = raw

	c.execute("select * from books where author=?", (d[author],))

	return str(c.fetchall())

if __name__ == '__main__':
	trying_sqlite.run(debug=True)
