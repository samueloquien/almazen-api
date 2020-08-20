from almazen.db import db

class Products(db.Model):
    prod_id = db.Column(db.Integer, autoincrement='auto', primary_key=True)
    prod_name = db.Column(db.String(45), nullable=False)
    prod_info = db.Column(db.String(300))
    prod_brand = db.Column(db.String(45))
    prod_image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'))
    prod_barcode_id = db.Column(db.Integer, db.ForeignKey('barcodes.barcode_id'))

    def __repr__(self):
        return '<Product %r>' % self.prod_name
