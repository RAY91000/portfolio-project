from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.review import Review
from app.extensions import db

review_bp = Blueprint('reviews', __name__)

@review_bp.route('/challenge/<challenge_id>', methods=['POST'])
@login_required
def create_review(challenge_id):
    data = request.form
    text = data.get('text')
    rating = data.get('rating')

    review = Review(
        text=text,
        rating=int(rating),
        challenge_id=challenge_id,
        user_id=current_user.id
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review created"}), 201

@review_bp.route('/challenge/<challenge_id>', methods=['GET'])
def get_reviews(challenge_id):
    reviews = Review.query.filter_by(challenge_id=challenge_id).all()
    return jsonify([{
        "text": r.text,
        "rating": r.rating
    } for r in reviews])
