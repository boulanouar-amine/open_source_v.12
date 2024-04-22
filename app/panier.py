from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from . import db
from .models.panier import Panier
from .models.customer import Customer

panier_bp = Blueprint('panier', __name__)

# Route to create a new panier for a customer
@panier_bp.route('/paniers/new', methods=['POST'])
def create_panier():
    customer_id = request.form.get('customer_id')
    if not customer_id:
        return jsonify({'error': 'Customer ID is required'}), 400
    
    new_panier = Panier(customer_id=customer_id)
    db.session.add(new_panier)
    db.session.commit()
    return jsonify({'message': 'Panier created successfully', 'panier_id': new_panier.id}), 201

# Route to list all paniers
@panier_bp.route('/paniers', methods=['GET'])
def list_paniers():
    paniers = Panier.query.all()
    return render_template('list_paniers.html', paniers=paniers)

# Route to view a single panier
@panier_bp.route('/paniers/<int:id>', methods=['GET'])
def get_panier(id):
    panier = Panier.query.get_or_404(id)
    return render_template('view_panier.html', panier=panier)

# Route to delete a panier
@panier_bp.route('/paniers/delete/<int:id>', methods=['POST'])
def delete_panier(id):
    panier = Panier.query.get_or_404(id)
    db.session.delete(panier)
    db.session.commit()
    return redirect(url_for('panier.list_paniers'))

# Optionally, add routes for updating panier details if necessary
@panier_bp.route('/paniers/update/<int:id>', methods=['POST'])
def update_panier(id):
    panier = Panier.query.get_or_404(id)
    customer_id = request.form.get('customer_id')
    if customer_id:
        panier.customer_id = customer_id
    db.session.commit()
    return jsonify({'message': 'Panier updated successfully'})
