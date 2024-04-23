from . import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    latitude = db.Column(db.Float,nullable=False)
    longitude = db.Column(db.Float,nullable=False)
    
    road = db.Column(db.String(128), nullable=True)
    quarter = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    county = db.Column(db.String(128), nullable=True)
    state_district = db.Column(db.String(128), nullable=True)
    region = db.Column(db.String(128), nullable=True)
    postcode = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(128), nullable=True)
    country_code = db.Column(db.String(2), nullable=True)


    is_source = db.Column(db.Boolean, default=False, nullable=False)
    is_destination = db.Column(db.Boolean, default=False, nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=True)
    customer = db.relationship('Customer', back_populates='address')
