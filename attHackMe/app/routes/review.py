from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.review import Review
from app.extensions import db
from app.models.progress import Progress 

review_bp = Blueprint('reviews', __name__)

@review_bp.route('/challenge/<challenge_id>', methods=['POST'])
@login_required
def create_review(challenge_id):
    # 1. Vérifie si l'utilisateur a complété le challenge
    progress = Progress.query.filter_by(
        user_id=current_user.id,
        challenge_id=challenge_id,
        status='completed'
    ).first()

    if not progress:
        return jsonify({"error": "You must complete the challenge before reviewing it."}), 403

    # 2. Si déjà review, refuse
    existing = Review.query.filter_by(user_id=current_user.id, challenge_id=challenge_id).first()
    if existing:
        return jsonify({"error": "You already reviewed this challenge."}), 400

    # 3. Crée la review
    data = request.form
    review = Review(
        text=data.get('text'),
        rating=int(data.get('rating')),
        challenge_id=challenge_id,
        user_id=current_user.id
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review created"}), 201

