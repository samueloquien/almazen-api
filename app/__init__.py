# server/__init__.py

import os
from flask import Flask, request, jsonify, abort, Response
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource
from flask_jwt_extended import JWTManager, jwt_optional, jwt_required, get_jwt_identity, create_access_token, get_jwt_claims
try:
    app = Flask('almazen-api')
    try:
        print('os.environ[APP_SETTINGS]:',os.environ['APP_SETTINGS'])
        app.config.from_object(os.environ['APP_SETTINGS'])
    except KeyError:
        #app.config.from_object('config.DevelopmentConfig')
        print('setting TestingConfig')
        app.config.from_object('config.TestingConfig')
        print('finished setting config to TestingConfig')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print('config:',app.config)

    myjwt = JWTManager(app)
    @myjwt.user_claims_loader
    def add_claims_to_access_token(identity):
        role_id = Users.query.get(identity).user_role_id
        role = UserRoles.query.get(role_id).user_role
        return {'role': role}


    api = Api(
        title='Almazen API',
        version='0.0.1',
        description='API for executing commands and requesting data available from Almazen service',
    )
    api.init_app(app)

    db = SQLAlchemy(app)

    from app.models.languages import Languages
    from app.models.users import Users
    from app.models.barcodes import Barcodes
    from app.models.images import Images
    from app.models.labels import Labels
    from app.models.items_labels import ItemsLabels
    from app.models.products import Products
    from app.models.items import Items
    from app.models.user_roles import UserRoles

    from app.endpoints.user_ep import UserEP
    from app.endpoints.auth_ep import AuthLoginEP

    from app.endpoints.common import JsonResponse
    app.response_class = JsonResponse

    @app.route('/langs')
    def langs():
        languages = db.session().query(Languages).all()
        result = ", ".join([l.language_lang for l in languages])
        if not languages:
            result = "no languages defined"
        return result

    @app.route('/langs/add/<newlang>')
    def addlang(newlang):
        if newlang in langs():
            return 'Failed to add language ' + newlang + ' because it already exists.'
        app.logger.info('Adding language '+newlang)
        l = Languages(language_lang=newlang)
        app.logger.info('Language creaeted:', l)
        db.session().add(l)
        db.session().commit()
        return langs()

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


except Exception as err:
    app.logger.critical("Exception during application init: %s", err)
    app.logger.exception("Exception")
