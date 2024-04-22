from . import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    road = db.Column(db.String(128), nullable=True)
    quarter = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=False)
    county = db.Column(db.String(128), nullable=True)
    state_district = db.Column(db.String(128), nullable=True)
    region = db.Column(db.String(128), nullable=True)
    postcode = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(128), nullable=False)
    country_code = db.Column(db.String(2), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False, unique=True)
    customer = db.relationship('Customer', back_populates='address')
