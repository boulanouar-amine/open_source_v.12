from . import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    panier_id = db.Column(db.Integer, db.ForeignKey('paniers.id')) 
    id_customer = db.Column(db.Integer, nullable=False)
    id_produit = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    start_delivery_date = db.Column(db.Date, nullable=False)
    end_delivery_date = db.Column(db.Date, nullable=False)
    delivery_address = db.Column(db.String, nullable=False)
    total = db.Column(db.Float, nullable=False)