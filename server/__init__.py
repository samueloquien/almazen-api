# server/__init__.py

try:

    from flask import Flask

    app = Flask('almazen-api')

    from flask_restx import Api

    api = Api(
        title='Almazen API',
        version='0.0.1',
        description='API for executing commands and requesting data available from Almazen service',
    )
    api.init_app(app)


    @app.route('/hi')
    def index():
        return "Hello, World!"

    if __name__ == '__main__':
        app.run(debug=True)

except Exception as e:
    app.logger.critical("Exception during application init: %s", e)
    app.logger.exception("Exception")
