"""
Connect with Facebook ads API to add hashed emails to an existing CustomAudience. 

Return view of data from Facebook API and this services db.

http://crm-helper-app.herokuapp.com/
"""

import requests
import json
import os
import urlparse

import psycopg2
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

urlparse.uses_netloc.append("postgres")
db_url = urlparse.urlparse(os.environ["DATABASE_URL"])

with open('token.txt', 'r') as f:
	token = f.read().strip("\'\"")  # read token from local file for security

def file_validation(filename):
	return len(filename.split('.')) > 0  # TODO file validation that checks file type should move to client (Javascript)

def cleaner(raw_data):
	return [hash.strip('", ').lower() for hash in raw_data if hash and len(hash)>20]

def batcher(data):
	return [data[num:num+10000] for num in range(0,len(data)-1,10000)]  # batch email hashes into lists of 10k

def create_api_request(hash_batch,custom_audience_id):
	'''Attempted with Python SDK but this API endpoint returned a generic error'''
	internal_payload = {}
	internal_payload["data"] = hash_batch
	internal_payload["schema"] = "EMAIL_SHA256"
	jsonify_internal_payload = json.dumps(internal_payload) #PAYLOAD MUST BE JSON OBJECT, IF NOT WILL RETURN "(#100) Missing schema attribute in payloads"

	external_payload = {}
	external_payload['access_token'] = token
	external_payload['payload'] = jsonify_internal_payload

	url = 'https://graph.facebook.com/v2.3/{}/users'.format(custom_audience_id)

	r = requests.post(url, data=external_payload, verify=False)
	
	return r.text

@app.route('/', methods=['GET','POST'])
def upload_file():
	if request.method == 'POST':
		uploaded_file = request.files['file']
		filename = uploaded_file.filename
		if file_validation(filename):
			custom_audience_id = request.form['custom_audience_id']
			raw_data = uploaded_file.read().split('\r\n')
			data = cleaner(raw_data)
			file_count = str(len(data))
			batches = batcher(data)	

			fb_num_received = 0
			fb_num_invalid_entries = 0
			fb_invalid_entry_samples = []

			for i, batch in enumerate(batches):
				facebook_response = json.loads(create_api_request(batch,custom_audience_id))
				fb_num_received += facebook_response['num_received']
				fb_num_invalid_entries += facebook_response['num_invalid_entries']
				if facebook_response['invalid_entry_samples']:
					fb_invalid_entry_samples.append(facebook_response['invalid_entry_samples'])

			# TODO move data model to SQLAlchemy objects 
			conn = psycopg2.connect("dbname={} user={} password={} host={} ".format(db_url.path[1:], db_url.username, db_url.password, db_url.hostname))
			cur = conn.cursor()

			cur.execute("select * from information_schema.tables where table_name='crm_uploads'")
			exists = cur.fetchall()

			if not exists:
			#cur.execute("DROP TABLE IF EXISTS crm_uploads")
				cur.execute("CREATE TABLE crm_uploads(id serial primary key, custom_audience_id bigint,filename text, upload_timestamp timestamp default current_timestamp, file_count bigint,fb_num_received bigint, fb_num_invalid_entries bigint, fb_invalid_entry_samples text)")

			insert = """INSERT INTO crm_uploads(custom_audience_id, filename, file_count, fb_num_received, fb_num_invalid_entries, fb_invalid_entry_samples) VALUES ({}, '{}', {}, {}, {}, '{}')""".format(custom_audience_id, filename, file_count, fb_num_received, fb_num_invalid_entries, fb_invalid_entry_samples)
			cur.execute(insert)
			conn.commit()
			conn.close()
			return redirect(url_for('get_custom_audience_data', custom_audience_id=custom_audience_id))
	return render_template('upload.html')

@app.route('/<custom_audience_id>')
def get_custom_audience_data(custom_audience_id):
	url = 'https://graph.facebook.com/v2.3/{}?access_token={}&fields=id,account_id,name,approximate_count,data_source,delivery_status,operation_status,subtype'.format(custom_audience_id,token)
	select = 'SELECT * FROM crm_uploads WHERE custom_audience_id={} ORDER BY upload_timestamp DESC'.format(custom_audience_id)

	if custom_audience_id:
		conn = psycopg2.connect("dbname={} user={} password={} host={} ".format(db_url.path[1:], db_url.username, db_url.password, db_url.hostname))
		cur = conn.cursor()
		cur.execute(select)  #returning 'OperationalError: no such column: favicon.ico' but not affecting functionality, likely due to sqlite3 idiosyncracy 
		db_data = cur.fetchall()
		conn.close()

		if not db_data:
			db_data = 'No data uploaded to this custom audience via this tool'

		fb_data = json.loads(requests.get(url, verify=False).text)

	return render_template('return_data.html',
							custom_audience_id=custom_audience_id,
							fb_data=fb_data,
							db_data=db_data)

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
