from almazen import db
from almazen.models import *

from datetime import datetime
import json
from hamcrest import assert_that, equal_to
#from flask import propagate_exceptions

class TestConvenientMethods:
	def __init__(self, client):
		self.client = client
		self.access_token = ''
		self.responses = []

	def reset_db(self):
		print('Resetting DB...')

		Users.query.delete()
		db.session.execute('''ALTER TABLE users AUTO_INCREMENT = 1''')

		Languages.query.delete()
		db.session.execute('''ALTER TABLE languages AUTO_INCREMENT = 1''')
		db.session.add(Languages(language_lang='en-US'))

		UserRoles.query.delete()
		db.session.execute('''ALTER TABLE user_roles AUTO_INCREMENT = 1''')
		db.session.add(UserRoles(user_role='admin'))
		db.session.add(UserRoles(user_role='user'))
		
		db.session.commit()
		print('Done. DB was reset.')


	'''

	Users
	---------------------------------------------------------------------------
	'''

	def create_user(self, email, password, language_id=1, first_name=None, last_name=None,
		address=None, country=None, city=None, role_id=2):
		user = Users(user_email=email, user_create_datetime=datetime.now(), 
			user_first_name=first_name, user_address=address, user_country=country,
			user_city=city, user_language_id=language_id, user_role_id=role_id)
		user.hash_password(password)
		db.session.add(user)
		db.session.commit()

	def user_exists(self, email):
		u = Users.query.filter_by(user_email=email).first()
		return u is not None
	

	'''

	API calls
	---------------------------------------------------------------------------
	'''

	def call_api_get(self, endpoint_name, headers = {}):
		if self.access_token:
			headers['Authorization'] = 'Bearer ' + self.access_token
		
		response = self.client.get(
			endpoint_name,
			content_type = 'application/json',
			headers = headers
		)
		self.responses.append(response)
		return response, json.loads(response.data.decode())
	
	def call_api_post(self, endpoint_name, body = {}, headers = {}):
		if self.access_token:
			headers['Authorization'] = 'Bearer ' + self.access_token
		
		response = self.client.post(
			endpoint_name,
			content_type = 'application/json',
			data = json.dumps(body),
			headers = headers
		)
		self.responses.append(response)
		return response, json.loads(response.data.decode())	
	
	def call_api_patch(self, endpoint_name, body = {}, headers = {}):
		print('access_token:', self.access_token)
		if self.access_token:
			headers['Authorization'] = 'Bearer ' + self.access_token
			headers['Content-Type'] = 'application/json'
			print('setting headers:',headers)
		print('config:',app.config)
		
		response = self.client.patch(
			endpoint_name,
			content_type = 'application/json',
			data = json.dumps(body),
			headers = headers
		)
		print('flag7')
		#assert(1==2)
		self.responses.append(response)
		assert_that(2, equal_to(2), 'impossible is nothing')
		return response, json.loads(response.data.decode())	

	def call_api_delete(self, endpoint_name, headers = {}):
		if self.access_token:
			headers['Authorization'] = 'Bearer ' + self.access_token
		
		response = self.client.delete(
			endpoint_name,
			content_type = 'application/json',
			headers = headers
		)
		self.responses.append(response)
		return response, json.loads(response.data.decode())

	''' Returns response data as a Json object '''
	def get_response_data(self, index= -1):
		r = self.responses[index]
		data = json.loads(r.data.decode())
		return data

