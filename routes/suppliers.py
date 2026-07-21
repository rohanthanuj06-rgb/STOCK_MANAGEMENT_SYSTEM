from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import Supplier
from extensions import db

suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')

@suppliers_bp.route('/')
@login_required
def index():
    suppliers = Supplier.query.all()
    return render_template('suppliers/index.html', suppliers=suppliers)

@suppliers_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        contact_email = request.form.get('contact_email')
        contact_phone = request.form.get('contact_phone')
        address = request.form.get('address')
        
        supplier = Supplier(
            name=name,
            contact_email=contact_email,
            contact_phone=contact_phone,
            address=address
        )
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier added successfully!', 'success')
        return redirect(url_for('suppliers.index'))
        
    return render_template('suppliers/add.html')
