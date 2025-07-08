from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(username="Raphael").first()

    if user:
        user.points = 320
        user.rank = "Gold"
        user.soldier_skin = "soldat3.png"
        user.avatar = "avatar.png"
        user.banner = "banner.png"
        user.email_public = True  # pour voir l'email
        db.session.commit()
        print("✅ Utilisateur mis à jour !")
    else:
        print("❌ Utilisateur non trouvé")
