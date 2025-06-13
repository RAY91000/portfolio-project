from flask import Flask
from flask_cors import CORS
from app.extensions import db, login_manager, bcrypt, jwt, csrf
from app.routes.auth import auth_bp
from app.routes.user import user_bp
from app.routes.challenge import challenge_bp
from app.routes.review import review_bp
from app.routes.submission import submission_bp
from config import config as config_dict

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    app.config['WTF_CSRF_ENABLED'] = False  # désactive CSRF pour les tests
    CORS(app)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    csrf.init_app(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(challenge_bp, url_prefix="/challenges")
    app.register_blueprint(review_bp, url_prefix="/reviews")
    app.register_blueprint(submission_bp, url_prefix="/submissions")

    return app
