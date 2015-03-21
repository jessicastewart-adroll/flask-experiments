import sqlite3

def entry_creator(chunk):
	list_ = []
	syn = ''
	for i, line in enumerate(chunk.splitlines()):
		if i == 0:
			list_.append(line.split('TITLE: ')[1])
		elif i == 1:
			list_.append(line.split('AUTHOR: ')[1])
		elif i == 2:
			syn += line.split('SYNOPSIS: ')[1]
		else:
			syn += line

	list_.append(syn)

	return tuple(list_)

chunks = open('test.txt','r').read().split('\n\n')
parameters  = [entry_creator(chunk) for chunk in chunks if chunk]

conn = sqlite3.connect('test.db')
conn.text_factory = str
c = conn.cursor()
c.execute('create table books(title, author, synopsis)')
c.executemany('insert into books values (?,?,?)', parameters)
conn.commit()
conn.close()
