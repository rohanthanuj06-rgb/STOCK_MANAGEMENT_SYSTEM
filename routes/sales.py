from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Sale, SaleItem, Product, StockAuditLog
from extensions import db

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

@sales_bp.route('/')
@login_required
def index():
    sales = Sale.query.order_by(Sale.created_at.desc()).all()
    return render_template('sales/index.html', sales=sales)

@sales_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity') or 0)
        
        if not product_id or quantity <= 0:
            flash('Invalid product or quantity', 'danger')
            return redirect(url_for('sales.add'))
            
        product = Product.query.get(product_id)
        if product.available_stock < quantity:
            flash(f'Insufficient stock! Only {product.available_stock} available.', 'danger')
            return redirect(url_for('sales.add'))
            
        # Create Sale
        sale = Sale(user_id=current_user.id, customer_name=customer_name)
        db.session.add(sale)
        db.session.flush() # Get sale ID
        
        # Create Sale Item
        price = product.base_price
        item = SaleItem(sale_id=sale.id, product_id=product.id, quantity=quantity, price_per_unit=price)
        db.session.add(item)
        
        # Update Total
        sale.total_amount = quantity * price
        
        # Deduct Stock
        product.available_stock -= quantity
        
        # Audit Log
        log = StockAuditLog(
            product_id=product.id,
            user_id=current_user.id,
            change_type='Sale',
            quantity_changed=-quantity,
            new_available_stock=product.available_stock,
            reason=f"Sale #{sale.id}"
        )
        db.session.add(log)
        
        db.session.commit()
        flash('Sale recorded successfully!', 'success')
        return redirect(url_for('sales.index'))
        
    products = Product.query.filter(Product.available_stock > 0).all()
    return render_template('sales/add.html', products=products)
