# server/__init__.py

import os
from flask import Flask, request, jsonify, abort, Response
from flask_restx import Resource
from .jwt import jwt
from .db import db
from .apis import api

def create_app(config=None):

    app = Flask('almazen')
    configString = os.environ.get('APP_SETTINGS')
    if configString is None:
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object(configString)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    jwt.init_app(app)

    db.init_app(app)

    api.init_app(app)

    '''
    from app.endpoints.common import JsonResponse
    app.response_class = JsonResponse
    '''

    return app

