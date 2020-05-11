from app import db

class ItemsLabels(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    label_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<ItemsLabels %r-%r>' % (self.item_id, self.label_id)
