from flask import Blueprint, request, redirect, url_for, render_template
from .. import db
from ..models.product import Product

product_bp = Blueprint('product', __name__)


@product_bp.route('/products/new', methods=['POST', 'GET'])
def create_product():
    if request.method == 'POST':
        new_product = Product(nom=request.form['nom'], description=request.form['description'],
                              price=request.form['price'], weight=request.form['weight'])
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('product.list_products'))
    else:
        # For GET request, you might want to show a form to create a product
        return render_template('products/create_product.html')

@product_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)  # Use Product instead of product
    return render_template('products/view_product.html', product=product)


@product_bp.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return render_template('products/list_products.html', products=products)


@product_bp.route('/products/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product_to_delete = Product.query.get_or_404(
        id)  # Use Product instead of product
    db.session.delete(product_to_delete)
    db.session.commit()
    return redirect(url_for('product.list_products'))
