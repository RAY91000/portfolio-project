from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.submission import Submission
from app.models.challenge import Challenge
from app.extensions import db

submission_bp = Blueprint('submissions', __name__)

@submission_bp.route('/<challenge_id>', methods=['POST'])
@login_required
def submit_flag(challenge_id):
    submitted_flag = request.form.get('flag')
    challenge = Challenge.query.get_or_404(challenge_id)

    success = challenge.flag == submitted_flag
    submission = Submission(
        flag_submitted=submitted_flag,
        challenge_id=challenge.id,
        user_id=current_user.id,
        success=success
    )

    db.session.add(submission)
    db.session.commit()

    return jsonify({
        "success": success,
        "message": "Correct flag!" if success else "Incorrect flag."
    })
