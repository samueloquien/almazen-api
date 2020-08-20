import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    #SQLALCHEMY_DATABASE_URI = 'mysql://AlmazenAPI:S1403p++@localhost/almazen-db'
    SERVER_NAME = '127.0.0.1:5000'

    JWT_SECRET_KEY = 'my-super-secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1) 
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1) 


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://AlmazenAPI:S1403p++@localhost/almazen-db'


class TestingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://AlmazenAPI:S1403p++@localhost/almazen-db'
    PROPAGATE_EXCEPTIONS = True

