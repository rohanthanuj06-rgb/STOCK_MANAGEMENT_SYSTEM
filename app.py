from flask import Flask, render_template, redirect, url_for
from config import Config
from extensions import db, login_manager, migrate
from models import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints (to be created)
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.products import products_bp
    from routes.suppliers import suppliers_bp
    from routes.sales import sales_bp
    from routes.purchases import purchases_bp
    from routes.audit import audit_bp
    from routes.invoices import invoices_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(purchases_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(invoices_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
