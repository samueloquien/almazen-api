from app import db

class Language(db.Model):
    lang_id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Language %r>' % self.lang
