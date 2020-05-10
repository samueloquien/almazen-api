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

except Exception as err:
    app.logger.critical("Exception during application init: %s", err)
    app.logger.exception("Exception")
