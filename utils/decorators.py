from functools import wraps
from flask import abort
from flask_login import current_user
from extensions import login_manager

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def admin_required(fn):
    return role_required('Admin')(fn)

def manager_required(fn):
    return role_required('Admin', 'Manager')(fn)
