# server/__init__.py

import os
from flask import Flask, request, jsonify, abort, Response
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource

try:
    app = Flask('almazen-api')
    try:
        app.config.from_object(os.environ['APP_SETTINGS'])
    except KeyError:
        app.config.from_object('config.DevelopmentConfig')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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
    @app.route('/users')
    def users():
        users = db.session().query(Users).all()
        if not users:
            return 'No users defined'
        return ', '.join( [u.user_email for u in users] )

    from datetime import datetime
    import json
    @api.route('/users/add')
    class UsersEP(Resource):
        def post(self, *args, **kwargs):
            email = request.json.get('email')
            password = request.json.get('password')
            if email is None or password is None:
                abort(404)#Response('Missing arguments email and password')) # missing arguments
            if Users.query.filter_by(user_email=email).first() is not None:
                abort(404)#Response('User {} already exists.'.format(email))) # existing user
            lang_id = db.session().query(Languages).filter(Languages.language_lang=='en-US').one().language_id
            user = Users(user_email=email, user_language_id=lang_id, user_create_datetime=datetime.now())
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            #return jsonify({ 'email': user.user_email }), 200#, {'Location': url_for('get_user', id = user.id, _external = True)}
            return json.dumps({ 'email': user.user_email })

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
