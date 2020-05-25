from app import db

class UserRoles(db.Model):
    user_role_id = db.Column(db.Integer, autoincrement='auto', primary_key=True)
    user_role = db.Column(db.String(45), unique=True, nullable=False)

    def __repr__(self):
        return '<User role %r>' % self.user_role
