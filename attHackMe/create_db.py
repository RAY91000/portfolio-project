from app.extensions import db
from app.models.user import User
from app.models.challenge import Challenge
from app.models.progress import Progress
from app import create_app

app = create_app()

with app.app_context():
    print("🧨 Suppression et création de la base...")
    db.drop_all()
    db.create_all()
    print("✅ Base de données recréée avec succès !")
