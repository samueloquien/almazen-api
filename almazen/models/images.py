from almazen.db import db

class Images(db.Model):
    image_id = db.Column(db.Integer, autoincrement='auto', primary_key=True)
    image_path = db.Column(db.String(45))
    
    def __repr__(self):
        return '<Image %r>' % self.image_path
