from app import create_app

try:
	
	app = create_app()

	if __name__ == '__main__':
		app.run(debug=True)

except Exception as e:
    app.logger.critical("Exception during application init: %s", e)
    app.logger.exception("Exception")
