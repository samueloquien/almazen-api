from app import app, db

from app.models.languages import Languages
from app.models.users import Users
from app.models.barcodes import Barcodes
from app.models.images import Images
from app.models.labels import Labels
from app.models.items_labels import ItemsLabels
from app.models.products import Products
from app.models.items import Items
from app.models.user_roles import UserRoles

from datetime import datetime
import json

class TestConvenientMethods:
	def __init__(self, client):
		self.client = client
		self.__auth_token = ''
		self.responses = []

	def reset_db(self):
		print('Resetting DB...')

		Users.query.delete()
		db.session.execute('''ALTER TABLE users AUTO_INCREMENT = 0''')

		Languages.query.delete()
		db.session.execute('''ALTER TABLE languages AUTO_INCREMENT = 0''')
		db.session.commit()
		db.session.add(Languages(language_lang='en-US'))

		UserRoles.query.delete()
		db.session.execute('''ALTER TABLE user_roles AUTO_INCREMENT = 0''')
		db.session.commit()
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


	'''

	API calls
	---------------------------------------------------------------------------
	'''

	def call_api_get(self, endpoint_name, headers = {}):
		headers['Authorization'] = 'Bearer ' + self.__auth_token
		
		response = self.client.get(
			endpoint_name,
			content_type = 'application/json',
			headers = headers
		)
		self.responses.append(response)
		return response, json.loads(response.data.decode())
	
	def call_api_post(self, endpoint_name, body = {}, headers = {}):
		headers['Authorization'] = 'Bearer ' + self.__auth_token
		
		response = self.client.post(
			endpoint_name,
			content_type = 'application/json',
			data = json.dumps(body),
			headers = headers
		)
		self.responses.append(response)
		return response, json.loads(response.data.decode())	

	def call_api_delete(self, endpoint_name, headers = {}):
		headers['Authorization'] = 'Bearer ' + self.__auth_token
		
		response = self.client.delete(
			endpoint_name,
			content_type = 'application/json',
			headers = headers
		)
		self.responses.append(response)
		return response, json.loads(response.data.decode())
