from flask import Blueprint, render_template
from flask_login import login_required
from utils.decorators import admin_required
from models import StockAuditLog
from extensions import db

audit_bp = Blueprint('audit', __name__, url_prefix='/audit')

@audit_bp.route('/')
@login_required
@admin_required
def index():
    logs = StockAuditLog.query.order_by(StockAuditLog.created_at.desc()).all()
    return render_template('audit/index.html', logs=logs)
