from almazen.db import db

class Barcodes(db.Model):
    barcode_id = db.Column(db.Integer, autoincrement='auto', primary_key=True)
    barcode_code = db.Column(db.String(45))

    def __repr__(self):
        return '<Barcode %r>' % self.barcode_code
