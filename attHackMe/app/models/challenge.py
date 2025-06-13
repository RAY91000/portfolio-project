from app.extensions import db
from .base_model import BaseModel
import uuid

class Challenge(BaseModel):
    __tablename__ = 'challenges'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    flag = db.Column(db.String(100), nullable=False)
    docker_image = db.Column(db.String(100), nullable=True)
    instructions = db.Column(db.Text, nullable=True)


    def __repr__(self):
        return f"<Challenge {self.title}>"
