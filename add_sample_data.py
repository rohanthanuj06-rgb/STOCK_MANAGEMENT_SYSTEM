from app import create_app
from extensions import db
from models import User, Category, Supplier, Product, Sale, SaleItem, PurchaseOrder, PurchaseItem, StockAuditLog
import random
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # 1. Users
    if not User.query.filter_by(username='manager').first():
        manager = User(username='manager', email='manager@example.com', role='Manager')
        manager.set_password('manager123')
        db.session.add(manager)
    
    if not User.query.filter_by(username='staff').first():
        staff = User(username='staff', email='staff@example.com', role='Staff')
        staff.set_password('staff123')
        db.session.add(staff)
    
    db.session.commit()
    admin = User.query.filter_by(username='admin').first()
    manager = User.query.filter_by(username='manager').first()
    staff = User.query.filter_by(username='staff').first()

    # 2. Categories
    categories = ['Electronics', 'Clothing', 'Home Appliance', 'Furniture', 'Toys']
    db_categories = []
    for cat_name in categories:
        if not Category.query.filter_by(name=cat_name).first():
            cat = Category(name=cat_name, description=f'Various {cat_name}')
            db.session.add(cat)
            db_categories.append(cat)
    db.session.commit()
    
    if not db_categories:
        db_categories = Category.query.all()

    # 3. Suppliers
    suppliers = ['Global Techs', 'Fashion Hub', 'HomeGoods Inc', 'FurniStore', 'PlayKids']
    db_suppliers = []
    for sup_name in suppliers:
        if not Supplier.query.filter_by(name=sup_name).first():
            sup = Supplier(name=sup_name, contact_email=f'{sup_name.lower().replace(" ", "")}@example.com', contact_phone='1234567890', address=f'123 {sup_name} St')
            db.session.add(sup)
            db_suppliers.append(sup)
    db.session.commit()
    
    if not db_suppliers:
        db_suppliers = Supplier.query.all()

    # 4. Products (Add at least 15 to test pagination)
    products_data = [
        ('Laptop Pro', 'Electronics', 'Global Techs', 1200.0, 50),
        ('Smartphone X', 'Electronics', 'Global Techs', 800.0, 100),
        ('Wireless Mouse', 'Electronics', 'Global Techs', 25.0, 200),
        ('Mechanical Keyboard', 'Electronics', 'Global Techs', 75.0, 150),
        ('4K Monitor', 'Electronics', 'Global Techs', 300.0, 40),
        ('Mens T-Shirt', 'Clothing', 'Fashion Hub', 20.0, 300),
        ('Womens Jeans', 'Clothing', 'Fashion Hub', 40.0, 250),
        ('Sneakers', 'Clothing', 'Fashion Hub', 60.0, 150),
        ('Winter Jacket', 'Clothing', 'Fashion Hub', 100.0, 80),
        ('Summer Hat', 'Clothing', 'Fashion Hub', 15.0, 500),
        ('Blender', 'Home Appliance', 'HomeGoods Inc', 50.0, 60),
        ('Microwave Oven', 'Home Appliance', 'HomeGoods Inc', 150.0, 30),
        ('Coffee Maker', 'Home Appliance', 'HomeGoods Inc', 80.0, 70),
        ('Toaster', 'Home Appliance', 'HomeGoods Inc', 30.0, 100),
        ('Vacuum Cleaner', 'Home Appliance', 'HomeGoods Inc', 200.0, 25),
        ('Office Chair', 'Furniture', 'FurniStore', 120.0, 45),
        ('Dining Table', 'Furniture', 'FurniStore', 350.0, 15),
        ('Sofa Set', 'Furniture', 'FurniStore', 600.0, 10),
        ('Action Figure', 'Toys', 'PlayKids', 15.0, 200),
        ('Board Game', 'Toys', 'PlayKids', 25.0, 150),
    ]

    db_products = []
    for i, p_data in enumerate(products_data):
        name, cat_name, sup_name, price, stock = p_data
        cat = next((c for c in db_categories if c.name == cat_name), db_categories[0])
        sup = next((s for s in db_suppliers if s.name == sup_name), db_suppliers[0])
        
        sku = f'SKU-{cat.name[:3].upper()}-{i+1:04d}'
        if not Product.query.filter_by(sku=sku).first():
            product = Product(
                name=name,
                sku=sku,
                description=f'Description for {name}',
                base_price=price,
                category_id=cat.id,
                supplier_id=sup.id,
                available_stock=stock,
                minimum_threshold=10
            )
            db.session.add(product)
            db_products.append(product)
    db.session.commit()

    if not db_products:
        db_products = Product.query.all()

    # 5. Purchase Orders (Add at least 15)
    for i in range(15):
        sup = random.choice(db_suppliers)
        po = PurchaseOrder(
            supplier_id=sup.id,
            user_id=manager.id if manager else admin.id,
            status=random.choice(['Pending', 'Received']),
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
        )
        db.session.add(po)
        db.session.commit() # Commit to get ID
        
        total_amount = 0
        for _ in range(random.randint(1, 3)):
            prod = random.choice(db_products)
            qty = random.randint(10, 50)
            cost = prod.base_price * 0.8
            pi = PurchaseItem(
                purchase_order_id=po.id,
                product_id=prod.id,
                quantity=qty,
                cost_per_unit=cost
            )
            db.session.add(pi)
            total_amount += qty * cost
            
        po.total_amount = total_amount
        db.session.commit()

    # 6. Sales (Add at least 15)
    for i in range(15):
        sale = Sale(
            user_id=staff.id if staff else admin.id,
            customer_name=f'Customer {i+1}',
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 15))
        )
        db.session.add(sale)
        db.session.commit() # Commit to get ID
        
        total_amount = 0
        for _ in range(random.randint(1, 4)):
            prod = random.choice(db_products)
            qty = random.randint(1, 5)
            # Ensure not to sell more than stock if we want, but for sample data it's okay, maybe reduce available stock
            if prod.available_stock >= qty:
                prod.available_stock -= qty
                si = SaleItem(
                    sale_id=sale.id,
                    product_id=prod.id,
                    quantity=qty,
                    price_per_unit=prod.base_price
                )
                db.session.add(si)
                total_amount += qty * prod.base_price
                
                # Add Audit Log
                audit = StockAuditLog(
                    product_id=prod.id,
                    user_id=staff.id if staff else admin.id,
                    change_type='Sale',
                    quantity_changed=-qty,
                    new_available_stock=prod.available_stock,
                    reason=f'Sale #{sale.id}'
                )
                db.session.add(audit)
                
        sale.total_amount = total_amount
        db.session.commit()

    print("Sample data added successfully!")
