from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.progress import Progress
from app.models.challenge import Challenge
from flask import send_from_directory

profile_bp = Blueprint('profile', __name__)


@profile_bp.route("/profileview", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_profile():
    if request.method == "OPTIONS":
        return '', 204
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Load progress
    progress_entries = Progress.query.filter_by(user_id=user.id).all()
    progress = []
    completed_count = 0
    for p in progress_entries:
        ch = Challenge.query.get(p.challenge_id)
        if not ch:
            continue
        progress.append({
            "title": ch.title,
            "status": p.status
        })
        if p.status == "completed":
            completed_count += 1

    # Leveling system: every 5 challenges = +1 level
    level = completed_count // 5 + 1

    return jsonify({
        "username": user.username,
        "email": user.email if user.email_public else None,
        "level": level,
        "avatar_url": user.avatar_url,
        "banner_url": user.banner_url,
        "progress": progress,
        "email_public": user.email_public,
        "rank": user.rank,
        "points": user.points
    })



@profile_bp.route("/settings", methods=["PUT"])
@jwt_required()
def update_profile_settings():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    # Champs autorisés
    if "avatar_url" in data:
        user.avatar_url = data["avatar_url"]
    if "banner_url" in data:
        user.banner_url = data["banner_url"]
    if "email_public" in data:
        user.email_public = bool(data["email_public"])  # Cast vers bool

    db.session.commit()
    return jsonify({"message": "Profile updated successfully."}), 200


@profile_bp.route("/email_visibility", methods=["POST"])
@jwt_required()
def update_email_visibility():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if "is_public" not in data:
        return jsonify({"error": "Missing field 'is_public'"}), 400

    user.show_email = bool(data["is_public"])
    db.session.commit()
    return jsonify({"message": "Email visibility updated."}), 200

