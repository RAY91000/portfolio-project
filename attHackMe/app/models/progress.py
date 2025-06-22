from .base_model import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.extensions import db

class Progress(BaseModel):
    __tablename__ = "progress"

    user_id = db.Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(Integer, ForeignKey("challenges.id"), nullable=False)
    status = db.Column(String(20), default="started")  # started, completed, failed
    points = db.Column(db.Integer, default=0)

    user = relationship("User", back_populates="progress")
    challenge = relationship("Challenge", back_populates="progress")
