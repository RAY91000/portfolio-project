#!/usr/bin/env python3
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.challenge import Challenge
from app.models.review import Review

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Admin
    admin = User(
        username="admin",
        email="admin@att.com",
        is_admin=True
    )
    admin.set_password("admin1234")
    db.session.add(admin)

    # Utilisateur normal
    user = User(
        username="user",
        email="user@att.com",
        is_admin=False
    )
    user.set_password("user1234")
    db.session.add(user)

    # Challenge
    challenge = Challenge(
        title='Recon 101',
        description='Find open ports and basic services.',
        difficulty='Easy',
        category='Reconnaissance',
        flag='1337'
    )
    db.session.add(challenge)
    db.session.commit()

    # Review (par user sur le challenge)
    review = Review(
        text="Very instructive challenge!",
        rating=5,
        challenge_id=challenge.id,
        user_id=user.id
    )
    db.session.add(review)

    db.session.commit()
    print("✔ Base de données initialisée avec admin, user, challenge et review.")
