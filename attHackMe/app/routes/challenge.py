from flask import Blueprint, jsonify, request
from app.models.challenge import Challenge
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.extensions import db
from app.models.progress import Progress

challenge_bp = Blueprint('challenges', __name__)

@challenge_bp.route('/', methods=['GET'])
def get_challenges():
    challenges = Challenge.query.all()
    return jsonify([{
        "id": c.id,
        "title": c.title,
        "description": c.description,
        "difficulty": c.difficulty,
        "category": c.category,
        "flag": c.flag,
        "docker_image": c.docker_image,
        "instructions": c.instructions
    } for c in challenges])

@challenge_bp.route('/<uuid:id>', methods=['GET'])
@jwt_required(optional=True)
def get_challenge(id):
    challenge = Challenge.query.get_or_404(str(id))
    user_id = get_jwt_identity()
    can_review = False

    if user_id:
        progress = Progress.query.filter_by(user_id=user_id, challenge_id=str(id)).first()
        if progress and progress.status == "completed":
            can_review = True

    return jsonify({
        "id": str(challenge.id),
        "title": challenge.title,
        "description": challenge.description,
        "instructions": challenge.instructions,
        "difficulty": challenge.difficulty,
        "category": challenge.category,
        "flag": challenge.flag,
        "docker_image": challenge.docker_image,
        "can_review": can_review
    })

@challenge_bp.route('/<uuid:id>/start', methods=['POST'])
@jwt_required()
def start_challenge(id):
    user_id = get_jwt_identity()

    existing_progress = Progress.query.filter_by(user_id=user_id, challenge_id=str(id)).first()
    if existing_progress:
        return jsonify({"message": "Challenge already started"}), 201

    progress = Progress(
        user_id=user_id,
        challenge_id=str(id),
        status='started'
    )
    db.session.add(progress)
    db.session.commit()

    return jsonify({"message": "Challenge started successfully"}), 201

@challenge_bp.route("/validate_flag", methods=["POST", "OPTIONS"])
@jwt_required(optional=True)
def validate_flag():
    if request.method == "OPTIONS":
            response = jsonify({})
            response.status_code = 200
            return response

    data = request.get_json()
    submitted_flag = data.get("flag", "").strip()
    challenge_id = data.get("challenge_id")

    challenge = Challenge.query.get(challenge_id)
    if not challenge:
        return jsonify({"message": "Challenge introuvable"}), 404

    is_correct = submitted_flag == challenge.flag
    user_id = get_jwt_identity()

    progress = Progress.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
    if not progress:
        progress = Progress(user_id=user_id, challenge_id=challenge_id)
        db.session.add(progress)

    if is_correct:
        progress.status = "completed"
        db.session.commit()

    return jsonify({
        "message": "✅ Correct flag!" if is_correct else "❌ Incorrect flag.",
        "correct": is_correct
    })
