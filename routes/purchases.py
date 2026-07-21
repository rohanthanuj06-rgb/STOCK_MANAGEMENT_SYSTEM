from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import PurchaseOrder, PurchaseItem, Product, Supplier, StockAuditLog
from extensions import db

purchases_bp = Blueprint('purchases', __name__, url_prefix='/purchases')

@purchases_bp.route('/')
@login_required
def index():
    orders = PurchaseOrder.query.order_by(PurchaseOrder.created_at.desc()).all()
    return render_template('purchases/index.html', orders=orders)

@purchases_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        supplier_id = request.form.get('supplier_id')
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity') or 0)
        cost = float(request.form.get('cost') or 0.0)
        
        if not supplier_id or not product_id or quantity <= 0:
            flash('Please fill all required fields.', 'danger')
            return redirect(url_for('purchases.add'))
            
        order = PurchaseOrder(supplier_id=supplier_id, user_id=current_user.id, status='Completed')
        db.session.add(order)
        db.session.flush()
        
        item = PurchaseItem(purchase_order_id=order.id, product_id=product_id, quantity=quantity, cost_per_unit=cost)
        db.session.add(item)
        
        order.total_amount = quantity * cost
        
        # Increment stock
        product = Product.query.get(product_id)
        product.available_stock += quantity
        
        # Audit Log
        log = StockAuditLog(
            product_id=product.id,
            user_id=current_user.id,
            change_type='Purchase',
            quantity_changed=quantity,
            new_available_stock=product.available_stock,
            reason=f"Purchase Order #{order.id}"
        )
        db.session.add(log)
        
        db.session.commit()
        flash('Purchase Order created successfully!', 'success')
        return redirect(url_for('purchases.index'))
        
    suppliers = Supplier.query.all()
    products = Product.query.all()
    selected_product_id = request.args.get('product_id')
    return render_template('purchases/add.html', suppliers=suppliers, products=products, selected_product_id=selected_product_id)
