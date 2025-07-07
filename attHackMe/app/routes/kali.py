from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

kali_bp = Blueprint("kali", __name__)

@kali_bp.route("/start", methods=["POST"])
@jwt_required()
def start_kali_vm():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # URL d'accès direct à Guacamole avec les bons paramètres
    guac_url = (
        "http://127.0.0.1:8888/guacamole/#/client/"
    )

    return jsonify({
        "message": "VM Kali started",
        "guacamole_url": guac_url
    }), 200
