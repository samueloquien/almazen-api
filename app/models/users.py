from app import db

class Users(db.Model):
    user_id = db.Column(db.Integer, autoincrement='auto', primary_key=True)
    user_email = db.Column(db.String(255), unique=True, nullable=False)
    user_password = db.Column(db.String(32), nullable=False)
    user_create_datetime = db.Column(db.DateTime(3) , nullable=False)
    user_first_name = db.Column(db.String(45))
    user_last_name = db.Column(db.String(45))
    user_address = db.Column(db.String(255), nullable=False)
    user_country = db.Column(db.String(45))
    user_city = db.Column(db.String(45))
    user_language_id = db.Column(db.Integer, db.ForeignKey('languages.language_id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_email
