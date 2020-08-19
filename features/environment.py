from almazen import create_app
from features.convenient_methods import TestConvenientMethods

def before_feature(context, feature):
    app = create_app()
    if not 'localhost' in app.config.get('SQLALCHEMY_DATABASE_URI'):
        raise Exception('Disallowing a test on a non-local database')
    app.testing = True
    app.app_context().push()
    context.client = app.test_client()

    context._ = TestConvenientMethods(context.client)

def before_scenario(context, feature):
    print("Setting up for the next scenario test...")

    context._.reset_db()
