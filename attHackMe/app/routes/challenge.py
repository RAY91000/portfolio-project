from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.challenge import Challenge
from app.models.user import User
from app.models.progress import Progress
from app.decorators import admin_required

challenge_bp = Blueprint('challenges', __name__)

# Public: List all challenges
@challenge_bp.route("/", methods=["GET"])
def list_challenges():
    challenges = Challenge.query.all()
    return jsonify([{
        "id": str(ch.id),
        "title": ch.title,
        "description": ch.description,
        "difficulty": ch.difficulty,
        "category": ch.category,
        "flag": ch.flag,
        "docker_image": ch.docker_image,
        "instructions": ch.instructions
    } for ch in challenges]), 200

# Public: Get challenge detail
@challenge_bp.route("/<uuid:challenge_id>", methods=["GET"])
def get_challenge(challenge_id):
    ch = Challenge.query.get(str(challenge_id))
    if not ch:
        return jsonify({"error": "Challenge not found"}), 404

    return jsonify({
        "id": str(ch.id),
        "title": ch.title,
        "description": ch.description,
        "difficulty": ch.difficulty,
        "category": ch.category,
        "flag": ch.flag,
        "docker_image": ch.docker_image,
        "instructions": ch.instructions
    }), 200

# Authenticated: Start challenge and track progress
@challenge_bp.route("/<uuid:challenge_id>/start", methods=["POST"])
@jwt_required()
def start_challenge(challenge_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    ch = Challenge.query.get(str(challenge_id))
    if not ch:
        return jsonify({"error": "Challenge not found"}), 404

    existing = Progress.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
    if existing:
        return jsonify({"message": "Challenge already started"}), 200

    progress = Progress(user_id=user_id, challenge_id=challenge_id, status="started")
    db.session.add(progress)
    db.session.commit()
    return jsonify({"message": "Challenge started"}), 201

# Admin: Create a challenge
@challenge_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_challenge():
    data = request.get_json()
    required_fields = ["title", "description", "category", "difficulty"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    new_challenge = Challenge(**data)
    db.session.add(new_challenge)
    db.session.commit()
    return jsonify({
        "id": str(new_challenge.id),
        "title": new_challenge.title,
        "description": new_challenge.description,
        "difficulty": new_challenge.difficulty,
        "category": new_challenge.category,
        "flag": new_challenge.flag,
        "docker_image": new_challenge.docker_image,
        "instructions": new_challenge.instructions
    }), 201

# Admin: Update a challenge
@challenge_bp.route("/<uuid:challenge_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_challenge(challenge_id):
    ch = Challenge.query.get(str(challenge_id))
    if not ch:
        return jsonify({"error": "Challenge not found"}), 404

    data = request.get_json()
    for field in ["title", "description", "category", "difficulty", "instructions"]:
        if field in data:
            setattr(ch, field, data[field])

    db.session.commit()
    return jsonify({"message": "Challenge updated"}), 200

# Admin: Delete challenge
@challenge_bp.route("/<uuid:challenge_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_challenge(challenge_id):
    ch = Challenge.query.get(str(challenge_id))
    if not ch:
        return jsonify({"error": "Challenge not found"}), 404

    db.session.delete(ch)
    db.session.commit()
    return jsonify({"message": "Challenge deleted"}), 200
