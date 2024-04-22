from flask import Blueprint, request, redirect, url_for, render_template
from datetime import datetime
from .. import db
from ..models.order import Order
from ..models.product import Product
from ..models.customer import Customer

order_bp = Blueprint('order', __name__)


@order_bp.route('/orders/new', methods=['POST','GET'])
def create_order():
    if request.method == 'POST':
        new_order = Order(
            product_id=request.form.get('product_id'),
            quantity=request.form.get('quantity'),
            customer_id=request.form.get('customer_id'),

            start_delivery_date=datetime.strptime(
                request.form.get('start_delivery_date'), '%Y-%m-%dT%H:%M'),
            end_delivery_date=datetime.strptime(
                request.form.get('end_delivery_date'), '%Y-%m-%dT%H:%M')
        )
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('order.list_orders'))
    

    
    else:
        context = {
            "products": Product.query.all(),
            "customers": Customer.query.all()
        }
        return render_template('orders/create_order.html',**context)

# Route to view a single order


@order_bp.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = order.query.get_or_404(id)
    return render_template('orders/view_order.html', order=order)


@order_bp.route('/orders', methods=['GET'])
def list_orders():
    orders = Order.query.all()
    return render_template('orders/list_orders.html', orders=orders)


@order_bp.route('/orders/delete/<int:id>', methods=['POST'])
def delete_order(id):
    order_to_delete = Order.query.get_or_404(id)
    db.session.delete(order_to_delete)
    db.session.commit()
    return redirect(url_for('order.list_orders'))
