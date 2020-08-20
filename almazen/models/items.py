from almazen.db import db

class Items(db.Model):
    item_id = db.Column(db.Integer, autoincrement='auto', primary_key=True)
    item_prod_id = db.Column(db.Integer, db.ForeignKey('products.prod_id'), nullable=False)
    item_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    item_date_acquisition = db.Column(db.DateTime(3) , nullable=False)
    item_date_expiracy = db.Column(db.DateTime(3) , nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)
    item_percent_left = db.Column(db.Integer)

    def __repr__(self):
        return '<Item %r>' % self.item_id
