from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models.customer import Customer
from .models.product import Product
from .models.order import Order
from datetime import datetime



main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("base.html", title="Home")

@main.route('/customers')
def list_customers():
    customers = Customer.query.all()
    return render_template('list_customers.html', customers=customers)


@main.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        new_customer = Customer(nom=request.form['nom'], prenom=request.form['prenom'],
                                adresse=request.form['adresse'], telephone=request.form['telephone'])
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('main.list_customers')) 
    return render_template('add_customer.html')


@main.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    # Find the customer by ID
    customer_to_delete = Customer.query.get_or_404(customer_id)
    # Delete the customer from the database
    db.session.delete(customer_to_delete)
    db.session.commit()
    # Redirect to the list of customers, or another appropriate page
    return redirect(url_for('main.list_customers'))

@main.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('list_products.html', products=products)


@main.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        customer_id = request.form.get('customer_id')

        start_delivery_date = request.form.get('start_delivery_date')
        end_delivery_date = request.form.get('end_delivery_date')

        # Convert date strings to date objects
        start_datetime = datetime.strptime(start_delivery_date, '%Y-%m-%dT%H:%M')
        end_datetime = datetime.strptime(end_delivery_date , '%Y-%m-%dT%H:%M')

        new_order = Order(
            product_id=product_id,
            quantity=quantity,
            customer_id=customer_id,
  
            start_delivery_date=start_datetime,
            end_delivery_date=end_datetime
        )
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('main.home'))

    products = Product.query.all()
    customers = Customer.query.all()
    context = {"customers": customers, "products": products}
    return render_template('add_order.html', **context)


@main.route('/orders')
def list_orders():
    orders = Order.query.all()
    return render_template('list_orders.html', orders=orders)



@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Retrieve form data
        nom = request.form['nom']
        description = request.form['description']
        price = request.form['price']
        weight=request.form['weight']

        # Create new Product object
        new_product = Product(nom=nom, description=description, price=price,weight=weight)

        # Add to database and commit
        db.session.add(new_product)
        db.session.commit()

        # Redirect to some page, or you can redirect back to the same page to add another product
        return redirect(url_for('main.list_products'))  # Assuming you have a route to list products

    # If it's a GET request, just render the form
    return render_template('add_product.html')

