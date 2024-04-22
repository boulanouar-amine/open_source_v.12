from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models.customer import Customer

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
