from flask import Blueprint, jsonify, request
from app.models.review import Review
from app.models.progress import Progress
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

review_bp = Blueprint('reviews', __name__)

@review_bp.route('/challenge/<challenge_id>', methods=['POST'])
@jwt_required()
def create_review(challenge_id):
    user_id = get_jwt_identity()

    # 1. Vérifie que le challenge est complété
    progress = Progress.query.filter_by(
        user_id=user_id,
        challenge_id=challenge_id,
        status='completed'
    ).first()

    if not progress:
        return jsonify({"error": "You must complete the challenge before reviewing it."}), 403

    # 2. Vérifie l'absence de review existante
    existing = Review.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
    if existing:
        return jsonify({"error": "You already reviewed this challenge."}), 400

    # 3. Crée la review
    data = request.get_json()
    text = data.get('text')
    rating = data.get('rating')

    if not text or not rating:
        return jsonify({"error": "Text and rating are required"}), 400

    review = Review(
        text=text,
        rating=int(rating),
        challenge_id=challenge_id,
        user_id=user_id
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({"message": "Review created"}), 201
