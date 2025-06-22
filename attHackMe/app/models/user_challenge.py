from app.models.base_model import BaseModel
from app import db

class UserChallenge(BaseModel, db.Model):
    __tablename__ = "user_challenges"

    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.String(60), db.ForeignKey("challenges.id"), nullable=False)
    status = db.Column(db.String(20), default="pending")  # "pending", "solved"
    score = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "user_id": self.user_id,
            "challenge_id": self.challenge_id,
            "status": self.status,
            "score": self.score,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        })
        return data
