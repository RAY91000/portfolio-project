#!/usr/bin/env python3
import random
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.challenge import Challenge
from app.models.review import Review
from app.models.progress import Progress

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

        # Utilisateur principal
    main_user = User(
        username="raph",
        email="raphael.dott@hotmail.com",
        avatar_url="/static/images/avatar.png",
        banner_url="/static/images/banner.png",
        points=120,
        rank="#1",
        show_email=True
    )
    main_user.set_password("raph")
    db.session.add(main_user)

    # Utilisateurs fictifs
    for i in range(1, 10):
        u = User(
            username=f"user{i}",
            email=f"user{i}@att.com",
            avatar_url="/static/images/avatar.png",
            banner_url="/static/images/banner.png",
            points=100 - i * 10,          # Exemple de score décroissant
            rank=f"#{i+1}",                # Rang fictif
            show_email=False              # Tous masquent leur email
        )
        u.set_password(f"test{i}123")
        db.session.add(u)


    # Créer des challenges
    challenges = []
    for i in range(1, 10):
        c = Challenge(
            docker_image=f"att/chal{i}:latest",
            title=f"Challenge {i}",
            description=f"Description for challenge {i}.",
            instructions=f"Instruction set for challenge {i}.",
            difficulty=random.choice(['Easy', 'Medium', 'Hard']),
            category=random.choice(['Recon', 'Web', 'Crypto']),
            flag=f"flag{i}"
        )
        challenges.append(c)
        db.session.add(c)

    db.session.commit()

    # Ajouter progression + points fictifs
    for u in users:
        completed = random.sample(challenges, k=random.randint(1, len(challenges)))
        for ch in completed:
            prog = Progress(user_id=u.id, challenge_id=ch.id, status="completed", points=random.randint(10, 100))
            db.session.add(prog)

    # Ajouter pour le main user
    for ch in challenges[:3]:
        prog = Progress(user_id=main_user.id, challenge_id=ch.id, status="completed", points=30)
        db.session.add(prog)

    # Une review d’exemple
    review = Review(
        text="Very instructive challenge!",
        rating=5,
        challenge_id=challenges[0].id,
        user_id=main_user.id
    )
    db.session.add(review)

    db.session.commit()
    print("✔ Base de données initialisée avec utilisateurs, challenges, progressions et review.")
