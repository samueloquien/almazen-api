import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://AlmazenAPI:S1403p++@localhost/almazen-db'

