from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.progress import Progress

progress_bp = Blueprint("progress", __name__, url_prefix="/progress")

@progress_bp.route('/<uuid:challenge_id>/status', methods=['POST'])
@jwt_required()
def update_status(challenge_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    status = data.get("status", "started")

    prog = Progress.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
    if not prog:
        prog = Progress(user_id=user_id, challenge_id=challenge_id, status=status)
        db.session.add(prog)
    else:
        prog.status = status

    db.session.commit()
    return jsonify({"message": f"Progress updated to {status}."}), 200