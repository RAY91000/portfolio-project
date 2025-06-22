from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db
from app.decorators import admin_required
from functools import wraps

user_bp = Blueprint('users', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    return jsonify({
        "username": current_user.username,
        "email": current_user.email,
        "is_admin": current_user.is_admin
    })

# Route pour les admins (JWT) pour modifier un utilisateur
@user_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]

    db.session.commit()
    return jsonify({"message": "User updated"}), 200

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        identity = get_jwt_identity()
        if not identity:
            return jsonify({"error": "Missing or invalid token"}), 401

        user = User.query.get(identity)
        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403

        return f(*args, **kwargs)
    return decorated_function
