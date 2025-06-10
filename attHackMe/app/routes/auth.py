from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from app.extensions import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    print("➡️ register(): request.form =", request.form)
    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    
    try:
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Inscription réussie."}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Erreur lors de l'inscription."}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        login_user(user)
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
        return jsonify({
            "access_token": access_token,
            "user_id": user.id,
            "message": "Logged in"
        }), 200
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200
