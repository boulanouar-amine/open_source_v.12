from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models.customer import Customer
from .models.product import Product

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("base.html", title="Jinja and Flask")


@main.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        new_customer = Customer(nom=request.form['nom'], prenom=request.form['prenom'], adresse=request.form['adresse'], telephone=request.form['telephone'])
        db.session.add(new_customer)
        db.session.commit()
        return render_template('customers.html',customers=Customer.query.all())# Redirect to another page after successful submission
    return render_template('add_customer.html')


@main.route('/customers')
def list_products():
    products = Product.query.all()
    return render_template('list_customers.html', products=products)




@main.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('customers'))


@main.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('list_products.html', products=products)



@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Retrieve form data
        nom = request.form['nom']
        description = request.form['description']
        price = request.form['price']

        # Create new Product object
        new_product = Product(nom=nom, description=description, price=price)

        # Add to database and commit
        db.session.add(new_product)
        db.session.commit()

        # Redirect to some page, or you can redirect back to the same page to add another product
        return redirect(url_for('main.list_products'))  # Assuming you have a route to list products

    # If it's a GET request, just render the form
    return render_template('add_product.html')

