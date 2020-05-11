# server/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

try:
    app = Flask('almazen-api')
    try:
        app.config.from_object(os.environ['APP_SETTINGS'])
    except KeyError:
        app.config.from_object('config.DevelopmentConfig')


    api = Api(
        title='Almazen API',
        version='0.0.1',
        description='API for executing commands and requesting data available from Almazen service',
    )
    api.init_app(app)

    db = SQLAlchemy(app)

    from app.models.languages import Languages
    from app.models.users import Users

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

    @app.route('/users/add/<email>/<password>')
    def adduser(email,password):
        if email in users():
            return 'User already exists'
        lang_id = db.session().query(Languages).filter(Languages.language_lang=='english').one().language_id
        u = Users(user_email=email, user_password=password, user_language_id=lang_id )
        db.session().add(u)
        db.session().commit()
        return users()


except Exception as err:
    app.logger.critical("Exception during application init: %s", err)
    app.logger.exception("Exception")
