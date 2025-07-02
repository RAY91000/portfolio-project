from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.progress import Progress
from app.models.challenge import Challenge
from app.extensions import db

leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

@leaderboard_bp.route("/", methods=["GET"])
def get_leaderboard():
    # On récupère tous les utilisateurs et leur progression terminée
    users = User.query.all()
    leaderboard = []

    for user in users:
        completed = (
            db.session.query(Progress)
            .join(Challenge, Progress.challenge_id == Challenge.id)
            .filter(Progress.user_id == user.id, Progress.status == "completed")
            .all()
        )
        total_points = sum(progress.challenge.points for progress in completed)
        leaderboard.append({
            "username": user.username,
            "avatar_url": getattr(user, "avatar_url", None),
            "points": total_points
        })

    top_10 = sorted(leaderboard, key=lambda u: u["points"], reverse=True)[:10]
    return jsonify(top10), 200


@leaderboard_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_rank():
    current_user_id = get_jwt_identity()

    users = User.query.all()
    leaderboard = []

    for user in users:
        completed = (
            db.session.query(Progress)
            .join(Challenge, Progress.challenge_id == Challenge.id)
            .filter(Progress.user_id == user.id, Progress.status == "completed")
            .all()
        )
        total_points = sum(progress.challenge.points for progress in completed)
        leaderboard.append({
            "user_id": user.id,
            "username": user.username,
            "avatar_url": getattr(user, "avatar_url", None),
            "points": total_points
        })

    # Trier du plus grand au plus petit
    leaderboard.sort(key=lambda u: u["points"], reverse=True)

    # Trouver le rang du user
    for index, entry in enumerate(leaderboard):
        if entry["user_id"] == current_user_id:
            return jsonify({
                "rank": index + 1,
                "username": entry["username"],
                "points": entry["points"],
                "avatar_url": entry["avatar_url"]
            }), 200

    return jsonify({"error": "User not found in leaderboard"}), 404