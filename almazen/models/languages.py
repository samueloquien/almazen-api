from almazen.db import db

class Languages(db.Model):
    language_id = db.Column(db.Integer, primary_key=True)
    language_lang = db.Column(db.String(5), unique=True, nullable=False)

    def __repr__(self):
        return '<Language %r>' % self.lang
