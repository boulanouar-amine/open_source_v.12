from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from .. import db
from ..models.customer import Customer
from ..models.warehouse import Warehouse
from ..models.address import Address
from ..utils import reverse_geocode
import overpy

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customers/new', methods=['POST', 'GET'])
def create_customer():


    default_latitude = 32.87
    default_longitude = -6.93

    if request.method == 'POST':
        new_customer = Customer(
            nom=request.form['nom'],
            prenom=request.form['prenom'],
            telephone=request.form['telephone']
        )
        db.session.add(new_customer)
        db.session.commit() 

        latitude = request.form.get('latitude', default_latitude)
        longitude = request.form.get('longitude', default_longitude)

        address_data = reverse_geocode(latitude, longitude)

        if address_data is None:
            return jsonify({'error': 'Invalid coordinates'}), 400

        new_address = Address(latitude=latitude, longitude=longitude,
                            road = address_data.get('road', ''),
                            quarter=address_data.get('quarter', ''),
                            city=address_data.get('city', ''),
                            county=address_data.get('county', ''),
                            state_district=address_data.get('state_district', ''),
                            region=address_data.get('region', ''),
                            postcode=address_data.get('postcode', ''),
                            country=address_data.get('country', ''),
                            country_code=address_data.get('country_code', ''),
                            customer_id=new_customer.id
                            ,is_destination=True)
        db.session.add(new_address)
        db.session.commit()

        # Fetch the first warehouse as the source
        warehouse = Warehouse.query.first()
        if warehouse:
            source_latitude = warehouse.address.latitude
            source_longitude = warehouse.address.longitude

            latitude = float(latitude)
            longitude = float(longitude)
            api = overpy.Overpass()
            # Adjust the query to use a bounding box
            query = f"""
                [out:json];
                 node
                ({min(source_latitude, latitude)},{min(source_longitude, longitude)},
                 {max(source_latitude, latitude)},{max(source_longitude, longitude)});
                out body;
            """
            result = api.query(query)
            print(result.nodes)
            print(query)
            for element in result.nodes:

                address_instance = Address(latitude=element.lat, longitude=element.lon,
                            customer_id=new_customer.id
                            )
                    
                db.session.add(address_instance)
           
            db.session.commit()
            

        return redirect(url_for('customer.list_customers'))
    else:
        return render_template('customers/create_customer.html', latitude=default_latitude, longitude=default_longitude)

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

