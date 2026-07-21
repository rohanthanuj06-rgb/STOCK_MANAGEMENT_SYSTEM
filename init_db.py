from app import create_app
from extensions import db
from models import User

app = create_app()

with app.app_context():
    db.create_all()
    
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', role='Admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Database initialized and 'admin' user created.")
    else:
        print("Database already initialized.")
