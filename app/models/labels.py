from app import db

class Users(db.Model):
    label_id = db.Column(db.Integer, autoincrement='auto', primary_key=True)
    label = db.Column(db.String(45), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_email
