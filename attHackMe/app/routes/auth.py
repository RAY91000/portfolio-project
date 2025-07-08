from flask import Blueprint, request, jsonify, make_response, session
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from datetime import timedelta, datetime
from app.extensions import db
from app.models.user import User
from app.utils.mailer import send_email
import random
import re

auth_bp = Blueprint('auth', __name__)
email_otps = {}  # Dictionnaire temporaire: email -> (otp, expiration)

@auth_bp.route('/register', methods=['POST'])
def register():
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

    # Vérifie les critères de mot de passe
    password_regex = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$'
    )
    if not password_regex.match(password):
        return jsonify({
            "error": "Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial."
        }), 400

    # Crée utilisateur non vérifié
    user = User(username=username, email=email, is_verified=False)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Génère OTP et stocke temporairement
    otp = str(random.randint(100000, 999999))
    email_otps[email] = (otp, datetime.utcnow() + timedelta(minutes=10))

    # Envoie email
    send_email(email, "Code de vérification", f"Votre code est : {otp}")

    return jsonify({"message": "Inscription réussie. Vérifiez votre email pour le code."}), 201



@auth_bp.route('/verify_email', methods=['POST'])
def verify_email():
    data = request.get_json()
    email = data.get('email')
    otp_input = data.get('otp')

    if email not in email_otps:
        return jsonify({"error": "Aucun code trouvé pour cet email"}), 400

    otp_saved, expires_at = email_otps[email]
    if datetime.utcnow() > expires_at:
        del email_otps[email]
        return jsonify({"error": "Code expiré"}), 400

    if otp_input != otp_saved:
        return jsonify({"error": "Code incorrect"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    user.is_verified = True
    db.session.commit()
    del email_otps[email]

    return jsonify({"message": "Email vérifié avec succès"}), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    if not user.is_verified:
        return jsonify({"error": "Email non vérifié"}), 403

    if user.verify_password(password):
        login_user(user)
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))

        response = make_response(jsonify({
            "access_token": access_token,
            "user_id": user.id,
            "username": user.username,
            "message": "Logged in"
        }), 200)
        response.headers['Cache-Control'] = 'no-store'
        return response

    return jsonify({"error": "Identifiants invalides"}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200
