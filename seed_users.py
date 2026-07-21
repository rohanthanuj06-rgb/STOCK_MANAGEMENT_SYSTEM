from app import create_app
from extensions import db
from models import User

app = create_app()
with app.app_context():
    manager = User.query.filter_by(username='manager').first()
    if not manager:
        manager = User(username='manager', email='manager@test.com', role='Manager')
        manager.set_password('manager')
        db.session.add(manager)
        print("Manager created")
        
    staff = User.query.filter_by(username='sales').first()
    if not staff:
        staff = User(username='sales', email='sales@test.com', role='Staff')
        staff.set_password('sales')
        db.session.add(staff)
        print("Sales created")
        
    db.session.commit()
    print("Seed complete.")
