from . import db

class Product(db.Model):
    __tablename__ = 'products'  # Correct table name used in ForeignKey reference

    id = db.Column(db.Integer, primary_key=True)
    
    nom = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False) # Weight of the product in kg
    
