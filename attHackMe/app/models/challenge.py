from app.extensions import db
from .base_model import BaseModel

class Challenge(BaseModel):
    __tablename__ = 'challenges'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    flag = db.Column(db.String(100), nullable=False)
    docker_image = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Challenge {self.title}>"
