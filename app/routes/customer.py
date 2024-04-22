from ..utils import reverse_geocode
from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from .. import db
from ..models.customer import Customer
from ..models.address import Address
from ..utils import  reverse_geocode


customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customers/new', methods=['POST', 'GET'])
def create_customer():
    default_latitude = 32.89735584205886
    default_longitude = -6.914085770573746

    if request.method == 'POST':
        new_customer = Customer(nom=request.form['nom'],
                                prenom=request.form['prenom'],
                                telephone=request.form['telephone'])

        # First, add and commit the new_customer to ensure it gets an ID.
        db.session.add(new_customer)
        db.session.commit()  # Commit to assign an ID to new_customer

        latitude = request.form.get('latitude', default_latitude)
        longitude = request.form.get('longitude', default_longitude)

        address_data = reverse_geocode(latitude, longitude)
        if address_data is not None:
            # Now that new_customer has an ID, create the Address instance.
            address = Address(latitude=latitude, longitude=longitude,
                            road = address_data.get('road', ''),
                            quarter=address_data.get('quarter', ''),
                            city=address_data.get('city', ''),
                            county=address_data.get('county', ''),
                            state_district=address_data.get('state_district', ''),
                            region=address_data.get('region', ''),
                            postcode=address_data.get('postcode', ''),
                            country=address_data.get('country', ''),
                            country_code=address_data.get('country_code', ''),
                            customer_id=new_customer.id)
        else:
            return jsonify({'error': 'Invalid coordinates'}), 400
        
        db.session.add(address)
        db.session.commit()  

        return redirect(url_for('customer.list_customers'))
    else:
        return render_template('customers/create_customer.html',
                               latitude=default_latitude, longitude=default_longitude)

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

