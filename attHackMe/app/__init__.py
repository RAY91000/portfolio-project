from flask import Flask
from flask_cors import CORS
from app.extensions import db, login_manager, bcrypt, jwt, csrf
from app.routes.auth import auth_bp
from app.routes.user import user_bp
from app.routes.challenge import challenge_bp
from app.routes.review import review_bp
from app.routes.profile import profile_bp
from app.routes.progress import progress_bp
from app.routes.leaderboard import leaderboard_bp
from config import config as config_dict
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
load_dotenv()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    app.config['WTF_CSRF_ENABLED'] = False  # désactive CSRF pour les tests
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'
    CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5001"}}, supports_credentials=True)


    JWTManager(app)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    csrf.init_app(app)

    from app.routes.kali import kali_bp
    app.register_blueprint(kali_bp)

    
    



    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(challenge_bp, url_prefix="/challenges")
    app.register_blueprint(review_bp, url_prefix="/reviews")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(progress_bp, url_prefix="/progress")
    app.register_blueprint(leaderboard_bp, url_prefix="/leaderboard")
    



    
    return app