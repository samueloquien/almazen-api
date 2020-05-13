from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
 
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

try:
	
	if __name__ == '__main__':
		manager.run()

except Exception as e:
    app.logger.critical("Exception during application init: %s", e)
    app.logger.exception("Exception")
