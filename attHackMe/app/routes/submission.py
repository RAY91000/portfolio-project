from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.submission import Submission
from app.models.challenge import Challenge
from app.models.user import User
from app.extensions import db

submission_bp = Blueprint('submissions', __name__)

@submission_bp.route('/', methods=['POST'])
@jwt_required()
def submit_flag():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    flag = data.get('flag_submitted')
    challenge_id = data.get('challenge_id')
    user_id = get_jwt_identity()

    if not all([flag, challenge_id]):
        return jsonify({"error": "Missing challenge_id or flag"}), 400

    challenge = Challenge.query.get_or_404(challenge_id)

    success = (flag == challenge.flag)

    submission = Submission(
        flag_submitted=flag,
        challenge_id=challenge.id,
        user_id=user_id,
        success=success
    )
    db.session.add(submission)
    db.session.commit()

    return jsonify({
        "success": success,
        "message": "✅ Flag correct !" if success else "❌ Mauvais flag."
    })
