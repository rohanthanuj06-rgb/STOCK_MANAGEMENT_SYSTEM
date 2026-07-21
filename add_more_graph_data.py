from app import create_app
from extensions import db
from models import User, Category, Supplier, Product, Sale, SaleItem, PurchaseOrder, PurchaseItem, StockAuditLog
import random
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    manager = User.query.filter_by(username='manager').first()
    staff = User.query.filter_by(username='staff').first()
    
    db_products = Product.query.all()
    db_suppliers = Supplier.query.all()

    if not db_products or not db_suppliers:
        print("Please run the initial sample data script first, or ensure products and suppliers exist.")
        exit()

    print("Generating large amount of historical data...")

    # Generate dates over the last 180 days (6 months)
    today = datetime.utcnow()
    
    # 1. More Purchase Orders (Add 80 more)
    print("Adding 80 historical Purchase Orders...")
    for i in range(80):
        sup = random.choice(db_suppliers)
        # Ensure many purchases in the last 7 days to populate graphs
        if random.random() > 0.5:
            random_days_ago = random.randint(0, 7)
        else:
            random_days_ago = random.randint(1, 180)
        po_date = today - timedelta(days=random_days_ago) + timedelta(hours=random.randint(1, 12))
        
        po = PurchaseOrder(
            supplier_id=sup.id,
            user_id=manager.id if manager else admin.id,
            status=random.choice(['Pending', 'Received']),
            created_at=po_date
        )
        db.session.add(po)
        db.session.commit() # Commit to get ID
        
        total_amount = 0
        for _ in range(random.randint(1, 4)):
            prod = random.choice(db_products)
            qty = random.randint(20, 100)
            cost = prod.base_price * 0.7 # 30% margin
            pi = PurchaseItem(
                purchase_order_id=po.id,
                product_id=prod.id,
                quantity=qty,
                cost_per_unit=cost
            )
            db.session.add(pi)
            total_amount += qty * cost
            
            if po.status == 'Received':
                # optionally increase stock and add audit log, but for historical data we just want the graph to look good. We will simulate stock increase
                prod.available_stock += qty
                audit = StockAuditLog(
                    product_id=prod.id,
                    user_id=manager.id if manager else admin.id,
                    change_type='Purchase',
                    quantity_changed=qty,
                    new_available_stock=prod.available_stock,
                    reason=f'Hist Purchase #{po.id}',
                    created_at=po_date
                )
                db.session.add(audit)
                
        po.total_amount = total_amount
        db.session.commit()

    # 2. More Sales (Add 300 more to make graph very active)
    print("Adding 300 historical Sales...")
    for i in range(300):
        random_days_ago = random.randint(1, 180)
        
        # Introduce a trend: more sales recently, especially in the last 7 days
        rand_val = random.random()
        if rand_val > 0.7:
            random_days_ago = random.randint(0, 7)
        elif rand_val > 0.3:
            random_days_ago = random.randint(1, 60)
            
        sale_date = today - timedelta(days=random_days_ago) + timedelta(hours=random.randint(8, 18))
        
        sale = Sale(
            user_id=staff.id if staff else admin.id,
            customer_name=f'Walk-in Customer {random.randint(100, 999)}',
            created_at=sale_date
        )
        db.session.add(sale)
        db.session.commit() # Commit to get ID
        
        total_amount = 0
        for _ in range(random.randint(1, 5)):
            prod = random.choice(db_products)
            qty = random.randint(1, 3)
            
            # For sample data graph, we might not care about going negative in stock, but let's try not to
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
                reason=f'Hist Sale #{sale.id}',
                created_at=sale_date
            )
            db.session.add(audit)
                
        sale.total_amount = total_amount
        db.session.commit()

    print("More graph data added successfully!")
