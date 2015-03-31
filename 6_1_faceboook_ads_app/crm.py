#connect with Facebook ads API to add hashed emails to an existing CustomAudience and get data for CustomAudience

import requests
import json

from flask import Flask, request, render_template

app = Flask(__name__)

with open('token.txt', 'r') as f:
	token = f.read().strip("\'\"") #read token from local file for security

def file_validation(filename):
	return len(filename.split('.')) > 0

def cleaner(raw_data):
	return [hash.strip('", ').lower() for hash in raw_data if hash and len(hash)>20]

def batcher(data):
	return [data[num:num+10000] for num in range(0,len(data)-1,10000)] #batch email hashes into lists of 10k

def create_api_request(hash_batch,custom_audience_id):
	internal_payload = {}
	internal_payload["data"] = hash_batch
	internal_payload["schema"] = "EMAIL_SHA256"
	jsonify_internal_payload = json.dumps(internal_payload) #PAYLOAD MUST BE JSON OBJECT, IF NOT WILL RETURN "(#100) Missing schema attribute in payloads"

	external_payload = {}
	external_payload['access_token'] = token
	external_payload['payload'] = jsonify_internal_payload

	url = 'https://graph.facebook.com/v2.3/{}/users'.format(custom_audience_id)

	r = requests.post(url, data=external_payload)
	
	return r.text

@app.route('/', methods=['GET','POST'])
def upload_file():
	if request.method == 'POST':
		hash_file = request.files['file']
		if hash_file and file_validation(hash_file.filename):
			custom_audience_id = request.form['custom_audience_id']
			raw_data = hash_file.read().split('\r\n')
			data = cleaner(raw_data)
			hash_num = str(len(data)) 
			batches = batcher(data)	
			batch_num = str(len(batches))
			facebook_requests = []
			for i, batch in enumerate(batches):
				print 'Processing batch {}'.format(str(i))
				facebook_requests.append(create_api_request(batch,custom_audience_id))
			return '{} hashes in file, {} batches\n\n\n'.format(hash_num, batch_num) + str(facebook_requests)
	return render_template('upload.html')

@app.route('/<custom_audience_id>')
def get_custom_audience_data(custom_audience_id):
	url = 'https://graph.facebook.com/v2.3/{}?access_token={}&fields=id,account_id,name,approximate_count,data_source,delivery_status,operation_status,subtype'.format(custom_audience_id,token)
	r = requests.get(url)
	return str(r.text)

if __name__ == '__main__':
	app.run(debug=True)
