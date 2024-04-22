from . import db

class Panier(db.Model):
    __tablename__ = 'paniers'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer = db.relationship('Customer', back_populates='panier')
    total = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', backref='panier')