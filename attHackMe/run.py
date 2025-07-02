from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.challenge import challenge_bp

# Créer l'application
app = Flask(__name__)

# Configuration du JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # change pour une vraie clé
app.config['JWT_TOKEN_LOCATION'] = ['headers']  # ou ['cookies'] si tu utilises les cookies
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

jwt = JWTManager(app)
# Activer CORS (autorise 5001 pour ton front)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5001"}}, supports_credentials=True)

# Enregistrer les blueprints
from app.routes.profile import profile_bp
from app.routes.challenge import challenge_bp

app.register_blueprint(profile_bp, url_prefix="/profile")
app.register_blueprint(challenge_bp, url_prefix="/challenges")


# Lancer le serveur backend (API)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
