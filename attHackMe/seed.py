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
    challenge1 = Challenge(
        docker_image='att/recon101:latest',
        title='Recon 101',
        description='Find open ports and basic services.',
        instructions="""
        You are given a target IP. Use tools like 'namp' or 'rustscan' to identify services.
        then, try connecting to those services manually and gather information.
        Hint: There might be a default webpage hidden somewhere.""",
        difficulty='Easy',
        category='Reconnaissance',
        flag='1337'
    )

    challenge2 = Challenge(
        docker_image='att/crypto101:latest',
        title='Crypto 101',
        description='Decrypt a simple message using a provided key.',
        difficulty='Medium',
        category='Cryptography',
        flag='crypto123'
    )
    challenge3 = Challenge(
        docker_image='att/web101:latest',
        title='Web 101',
        description='Find the hidden flag in a web application.',
        difficulty='Hard',
        category='Web',
        flag='webflag123'
    )
    challenges = [challenge1, challenge2, challenge3]
    for challenge in challenges:
        db.session.add_all(challenges)
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
