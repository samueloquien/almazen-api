from flask_restx import Api, Resource

from .ns_auth import api as ns1
from .ns_user import api as ns2

api = Api(
    title='Almazen API',
    version='0.0.1',
    description='API for executing commands and requesting data available from Almazen service',
)

api.add_namespace(ns1, path='/')
api.add_namespace(ns2, path='/')

'''
import json
# Export API as postman collection
try:
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    with app.app_context():
        data = api.as_postman(urlvars=urlvars, swagger=swagger)
        with open('postman_collection.json', 'w') as f:
            f.write(json.dumps(data, indent=2))
except Exception as err:
    print('Unable to export as postman: ', err)
    pass
'''
