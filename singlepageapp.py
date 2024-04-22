from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String)
    prenom = db.Column(db.String)
    adresse = db.Column(db.String)
    telephone = db.Column(db.String)

    panier = db.relationship('Panier', back_populates='customer', uselist=False)


class Panier(db.Model):
    __tablename__ = 'paniers'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer = db.relationship("Customer", back_populates="panier")
    total = db.Column(db.Float, nullable=False)
    orders = db.relationship("Order", backref='panier')  
 
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

class Product(db.Model):
    __tablename__ = 'products'  # Correct table name used in ForeignKey reference

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)

class Product_stock(db.Model):
    __tablename__ = 'product_stock'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Corrected ForeignKey reference
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)  # Link to Warehouse
    quantity = db.Column(db.Integer, nullable=False)
    
    product = db.relationship('Product', backref=db.backref('stock', lazy='select'))

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    id = db.Column(db.Integer, primary_key=True)
    product_stock_list = db.relationship("Product_stock", backref="warehouse")

    
@app.route("/")
def home():
    return render_template("base.html", title="Jinja and Flask")


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        new_customer = Customer(nom=request.form['nom'], prenom=request.form['prenom'], adresse=request.form['adresse'], telephone=request.form['telephone'])
        db.session.add(new_customer)
        db.session.commit()
        return render_template('customers.html',customers=Customer.query.all())# Redirect to another page after successful submission
    return render_template('add_customer.html')

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(debug=True)
