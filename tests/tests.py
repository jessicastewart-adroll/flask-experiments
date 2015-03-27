import unittest
import os

import sqlite3   
import werkzeug

import security

#integration tests for database 
class TestDatabaseTokening(unittest.TestCase):
	def setUp(self):
		self.conn = sqlite3.connect('security.db')
		self.cur = self.conn.cursor()

	def test_db_exists(self):
		self.assertTrue(os.path.isfile('security.db'))

	def test_users_table_exists(self):
		self.assertEqual(str(self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' and name='users'").fetchone()[0]), 'users')

	def test_for_sample_adam_row(self):
		self.assertEqual(str(self.cur.execute("SELECT username FROM users WHERE username='adam'").fetchone()[0]), 'adam')

	def test_password_hashed(self):
		hashed = str(self.cur.execute("SELECT password FROM users WHERE username='adam'").fetchone()[0])
		password = 'apple' 
		self.assertTrue(werkzeug.check_password_hash(hashed, password))

#unit tests for generating token view function
class TestTokening(unittest.TestCase):
	def setUp(self):
		security.app.config['TESTING'] = True
		self.test_app = security.app.test_client()

	def test_tokening_get(self):
		self.assertTrue('Please login' in self.test_app.get('/tokening').data)

	def test_tokening_post(self):
		self.assertTrue('WyJhZGFtIiwiYXBwbGUiXQ' in self.test_app.post('/tokening', data={'username':'adam', 'password':'apple'}).data)

	def test_tokenizing_bad_credentials(self):
		self.assertTrue('Please login' in self.test_app.post('/tokening', data={'username':'adam', 'password':'bad'}).data)

#unit tests for resource view function
class TestResource(unittest.TestCase):
	def setUp(self):
		security.app.config['TESTING'] = True
		self.test_app = security.app.test_client()
		self.fresh_token = self.test_app.post('/tokening', data={'username':'adam', 'password':'apple'}).data

	def test_resource_returns_data(self):
		rv = self.test_app.get('/resource?tokening={}'.format(self.fresh_token)).data
		self.assertTrue('DATA!' in rv)

	def test_bad_token(self):
		rv = self.test_app.get('/resource?tokening=bad').data
		self.assertTrue('Incorrect token' in rv)

	def test_expired_token(self):
		rv = self.test_app.get('/resource?tokening=WyJhZGFtIiwiYXBwbGUiXQ.B_MBMg.fSh7ZdTxdMyHaPTb-6fNnHqZeFQ').data
		self.assertTrue('Token expired')

if __name__ == '__main__':
	unittest.main()

#script to setup database with test data
'''
import os

import sqlite3   
import werkzeug

conn = sqlite3.connect('security.db')
cur = conn.cursor()

if not cur.execute("SELECT name FROM sqlite_master WHERE type='table' and name='users'").fetchone():
	cur.execute("CREATE TABLE users ('username', 'password')")

if not cur.execute("SELECT username FROM users WHERE username='adam'").fetchone():
	hashed = werkzeug.generate_password_hash('apple')
	cur.execute("INSERT INTO users VALUES ('adam', ?)", (hashed,))
	conn.commit()
'''
