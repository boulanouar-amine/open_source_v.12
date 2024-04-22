from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from .. import db
from ..models.customer import Customer

customer_bp = Blueprint('customer', __name__)


@customer_bp.route('/customers/new', methods=['POST','GET'])
def create_customer():
    if request.method == 'POST':
        new_customer = Customer(nom=request.form['nom'], prenom=request.form['prenom'],
                                    adresse=request.form['adresse'], telephone=request.form['telephone'])
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('customer.list_customers'))
    else:
    
        return render_template('customers/create_customer.html')

# Route to view a single customer


@customer_bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return render_template('customers/view_customer.html', customer=customer)


@customer_bp.route('/customers', methods=['GET'])
def list_customers():
    customers = Customer.query.all()
    return render_template('customers/list_customers.html', customers=customers)


@customer_bp.route('/customers/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('customer.list_customers'))

