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

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        firstname = db.Column(db.String(80))
        lastname = db.Column(db.String(80))

        def __repr__(self):
            return '<User %r>' % self.username

    @app.route('/hi')
    def index():
        return "Hello, World!"

except Exception as err:
    app.logger.critical("Exception during application init: %s", err)
    app.logger.exception("Exception")
