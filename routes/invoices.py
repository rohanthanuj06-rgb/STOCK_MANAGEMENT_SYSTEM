from flask import Blueprint, render_template, abort
from flask_login import login_required
from models import Sale

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')

@invoices_bp.route('/<int:sale_id>')
@login_required
def view(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    return render_template('invoices/view.html', sale=sale)
