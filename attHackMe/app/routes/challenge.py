from flask import Blueprint, jsonify
from app.models.challenge import Challenge

challenge_bp = Blueprint('challenges', __name__)

@challenge_bp.route('/', methods=['GET'])
def get_challenges():
    challenges = Challenge.query.all()
    return jsonify([{
        "id": c.id,
        "title": c.title,
        "description": c.description,
        "difficulty": c.difficulty
    } for c in challenges])
