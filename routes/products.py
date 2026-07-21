from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import Product, Category, Supplier
from extensions import db
import uuid

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/')
@login_required
def index():
    query = request.args.get('q', '')
    category_id = request.args.get('category_id')
    low_stock = request.args.get('low_stock')
    
    base_query = Product.query
    if query:
        base_query = base_query.filter(
            Product.name.ilike(f'%{query}%') | Product.sku.ilike(f'%{query}%')
        )
    if category_id:
        base_query = base_query.filter_by(category_id=category_id)
        
    products = base_query.all()
    
    if low_stock == '1':
        products = [p for p in products if p.stock_status in ['Low Stock', 'Out of Stock']]
        
    categories = Category.query.all()
    return render_template('products/index.html', products=products, categories=categories, query=query, selected_category=category_id, low_stock=low_stock)

@products_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        category_id = request.form.get('category_id')
        supplier_id = request.form.get('supplier_id')
        base_price = request.form.get('base_price')
        available_stock = request.form.get('available_stock')
        minimum_threshold = request.form.get('minimum_threshold')
        
        sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"
        
        product = Product(
            name=name,
            sku=sku,
            category_id=category_id if category_id else None,
            supplier_id=supplier_id if supplier_id else None,
            base_price=float(base_price) if base_price else 0.0,
            available_stock=int(available_stock) if available_stock else 0,
            minimum_threshold=int(minimum_threshold) if minimum_threshold else 10
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products.index'))
        
    categories = Category.query.all()
    suppliers = Supplier.query.all()
    return render_template('products/add.html', categories=categories, suppliers=suppliers)

@products_bp.route('/category/add', methods=['POST'])
@login_required
def add_category():
    name = request.form.get('name')
    if name:
        cat = Category(name=name)
        db.session.add(cat)
        db.session.commit()
        flash('Category added successfully.', 'success')
    return redirect(url_for('products.index'))
