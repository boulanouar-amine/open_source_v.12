from . import db

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String)
    prenom = db.Column(db.String)
    adresse = db.Column(db.String)
    telephone = db.Column(db.String)

    panier = db.relationship('Panier', back_populates='customer', uselist=False)
