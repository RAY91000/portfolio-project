from flask import Blueprint, jsonify
from app.models.challenge import Challenge
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.submission import Submission
from datetime import datetime
from app.extensions import db

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
def get_challenge(id):
    challenge = Challenge.query.get_or_404(str(id))
    return jsonify({
        "id": str(challenge.id),
        "title": challenge.title,
        "description": challenge.description,
        "instructions": challenge.instructions,
        "difficulty": challenge.difficulty,
        "category": challenge.category,
        "flag": challenge.flag,
        "docker_image": challenge.docker_image,
    })

@challenge_bp.route('/<uuid:id>/start', methods=['POST'])
@jwt_required()
def start_challenge(id):
    user_id = get_jwt_identity()
    
    # Check if the user has already started this challenge
    existing_submission = Submission.query.filter_by(user_id=user_id, challenge_id=str(id)).first()
    if existing_submission:
        return jsonify({"message": "Challenge already started"}), 201
    
    # Create a new submission
    submission = Submission(
        user_id=user_id,
        challenge_id=str(id),
        status='in_progress',
        created_at =datetime.utcnow()
    )
    
    db.session.add(submission)
    db.session.commit()
    
    return jsonify({"message": "Challenge started successfully", "submission_id": submission.id}), 201
