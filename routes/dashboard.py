from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Product, Sale, PurchaseOrder, StockAuditLog, Category, Supplier, SaleItem, PurchaseItem
from extensions import db
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    # Basic KPIs
    total_products = Product.query.count()
    total_sales = db.session.query(func.sum(Sale.total_amount)).scalar() or 0.0
    low_stock_count = Product.query.filter(Product.available_stock <= Product.minimum_threshold).count()
    pending_orders = PurchaseOrder.query.filter_by(status='Pending').count()
    
    today = datetime.utcnow().date()
    # 1. Sales Trends & Profit/Loss (Last 7 days)
    revenue_data = []
    cost_data = []
    profit_labels = []
    
    all_sales = Sale.query.all()
    all_purchases = PurchaseOrder.query.all()
    
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        daily_revenue = sum([s.total_amount for s in all_sales if s.created_at and s.created_at.date() == d])
        daily_cost = sum([p.total_amount for p in all_purchases if p.created_at and p.created_at.date() == d])
        revenue_data.append(daily_revenue)
        cost_data.append(daily_cost)
        profit_labels.append(d.strftime('%b %d'))
        
    # 2. Stock Distribution by Category (Doughnut)
    categories = Category.query.all()
    stock_labels = [c.name for c in categories]
    stock_data = [sum([p.available_stock for p in c.products.all()]) for c in categories]
    if not stock_labels:
        stock_labels = ['No Categories']
        stock_data = [100]

    # 3. Best Selling Products (Top 5 - Bar Chart)
    # Using python to sum up if sqlite syntax is too complex for prototyping
    products_all = Product.query.all()
    product_sales = []
    for p in products_all:
        total_sold = sum([item.quantity for item in p.sale_items])
        if total_sold > 0:
            product_sales.append({'name': p.name, 'sold': total_sold})
    
    product_sales.sort(key=lambda x: x['sold'], reverse=True)
    top_products = product_sales[:5]
    top_products_labels = [p['name'] for p in top_products]
    top_products_data = [p['sold'] for p in top_products]

    # 4. Compare Fast Selling Products in top category (Radar/Bar)
    compare_labels = []
    compare_data = []
    top_category_name = "N/A"
    if categories:
        # Find category with most products
        sorted_cats = sorted(categories, key=lambda c: c.products.count(), reverse=True)
        if sorted_cats:
            biggest_cat = sorted_cats[0]
            top_category_name = biggest_cat.name
            
            cat_sales = []
            for p in biggest_cat.products.all():
                sold = sum([item.quantity for item in p.sale_items])
                cat_sales.append({'name': p.name, 'sold': sold})
            cat_sales.sort(key=lambda x: x['sold'], reverse=True)
            
            top_cat_sales = cat_sales[:5]
            compare_labels = [c['name'] for c in top_cat_sales]
            compare_data = [c['sold'] for c in top_cat_sales]

    # 5. Supplier Cost Analysis (Average Unit Cost across goods - Scatter/Bar)
    supplier_labels = []
    supplier_costs = []
    suppliers = Supplier.query.all()
    for sup in suppliers:
        total_items = 0
        total_cost = 0
        for po in sup.purchases.all():
            for item in po.items.all():
                total_items += item.quantity
                total_cost += item.quantity * item.cost_per_unit
        avg_cost = (total_cost / total_items) if total_items > 0 else 0
        supplier_labels.append(sup.name)
        supplier_costs.append(avg_cost)

    return render_template('dashboard/index.html', 
                          total_products=total_products,
                          total_sales=total_sales,
                          low_stock_count=low_stock_count,
                          pending_orders=pending_orders,
                          # Chart 1: Sales & P/L
                          profit_labels=profit_labels,
                          revenue_data=revenue_data,
                          cost_data=cost_data,
                          # Chart 2: Category
                          stock_labels=stock_labels,
                          stock_data=stock_data,
                          # Chart 3: Best Sellers
                          top_products_labels=top_products_labels,
                          top_products_data=top_products_data,
                          # Chart 4: Category Compare
                          top_category_name=top_category_name,
                          compare_labels=compare_labels,
                          compare_data=compare_data,
                          # Chart 5: Supplier Costs
                          supplier_labels=supplier_labels,
                          supplier_costs=supplier_costs
                          )
