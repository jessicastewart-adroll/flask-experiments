#script to insert test usernames and passwords
#sqlite actually specifies slightly specific SQL syntax

import sqlite3
from werkzeug import generate_password_hash

conn = sqlite3.connect('security.db')
c = conn.cursor()

u = [('adam', 'apple'),
	('brittany', 'banana'),
	('carrie', 'cranberry'),
	('david', 'durian'),
	('eric', 'elderberry')]

hu = [(user[0], generate_password_hash(user[1])) for user in u]

c.executemany("INSERT INTO users('username','password') VALUES(?,?)", hu) 
conn.commit()
conn.close()
