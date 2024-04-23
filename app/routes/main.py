from flask import Blueprint, render_template
from ..models import db
from ..models.customer import Customer
from ..models.address import Address
import overpy

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/customers/map/<int:id>")
def map(id):
    # Fetch customer's address based on customer ID
    customer_address = Address.query.filter_by(customer_id=id, is_destination=True).first()
    if not customer_address:
        return "Customer address not found", 404

    # Assuming the source is marked with `is_source=True`
    source_address = Address.query.filter_by(is_source=True).first()
    if not source_address:
        return "Source address not found", 404

    # Prepare source and destination markers
    source_marker = {
        'lat': source_address.latitude,
        'lng': source_address.longitude,
        'label': 'Source',
        'type': 'source'
    }

    destination_marker = {
        'lat': customer_address.latitude,
        'lng': customer_address.longitude,
        'label': 'Customer',
        'type': 'destination'
    }

    # Query for intermediate node markers that are neither source nor destination but linked to the same customer
    node_markers = Address.query.filter(
        Address.customer_id == id, 
        Address.id != customer_address.id, 
        Address.is_source.is_(False),
        Address.is_destination.is_(False)
    ).all()

    markers = [source_marker, destination_marker]

    # Append node markers to the markers list
    for node in node_markers:
        node_marker = {
            'lat': node.latitude,
            'lng': node.longitude,
            'label': 'Intermediate Node',
            'type': 'node'
        }
        markers.append(node_marker)

    return render_template('map/view_map.html', markers=markers)
