from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in first.", "warning")
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash("You are not authorized to access this page.", "danger")
            return redirect(url_for('main.home'))  # Or another safe page
        return f(*args, **kwargs)
    return decorated_function

