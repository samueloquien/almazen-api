from app import app, db
from features.convenient_methods import TestConvenientMethods


def before_scenario(context, feature):
    print("Setting up for the next feature test...")
    if not 'localhost' in app.config.get('SQLALCHEMY_DATABASE_URI'):
        raise Exception('Disallowing a test on a non-local database')
    app.testing = True
    context.client = app.test_client()

    context._ = TestConvenientMethods(context.client)

    context._.reset_db()
