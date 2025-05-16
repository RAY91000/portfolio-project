from app.extensions import db
from .base_model import BaseModel

class Submission(BaseModel):
    __tablename__ = 'submissions'

    flag_submitted = db.Column(db.String(100), nullable=False)
    challenge_id = db.Column(db.String(36), db.ForeignKey('challenges.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    success = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Submission by user {self.user_id} on challenge {self.challenge_id}>"
