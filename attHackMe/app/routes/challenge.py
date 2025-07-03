from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.challenge import Challenge
import docker

challenge_bp = Blueprint('challenges', __name__)

@challenge_bp.route('/', methods=['GET'])
def get_challenges():
    challenges = Challenge.query.all()
    return jsonify([{
        "id": c.id,
        "title": c.title,
        "description": c.description,
        "difficulty": c.difficulty
    } for c in challenges])

@challenge_bp.route('/start/<challenge_id>', methods=['POST'])
@jwt_required()
def start_challenge(challenge_id):
    challenge = Challenge.query.get(challenge_id)
    if not challenge:
        return jsonify({"error": "Challenge not found"}), 404

    container_name = challenge.docker_image
    if not container_name:
        return jsonify({"error": "No Docker image specified for this challenge"}), 400

    try:
        client = docker.from_env()
        container = client.containers.get(container_name)

        if container.status != "running":
            container.start()

        ip = container.attrs["NetworkSettings"]["Networks"]["att_net"]["IPAddress"]

        return jsonify({
            "title": challenge.title,
            "description": challenge.description,
            "ip": ip,
            "status": container.status
        }), 200

    except docker.errors.NotFound:
        return jsonify({"error": f"Container '{container_name}' not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@challenge_bp.route('/page', methods=['GET'])
def challenge_page():
    return render_template('challenges.html')

@challenge_bp.route('/kali/start', methods=['POST'])
@jwt_required()
def start_kali():
    try:
        client = docker.from_env()
        container = client.containers.get("kali")

        if container.status != "running":
            container.start()

        return jsonify({
            "message": "Kali démarrée",
            "guacamole_url": "http://localhost:8080/guacamole/"
        }), 200

    except docker.errors.NotFound:
        return jsonify({"error": "Conteneur 'kali' introuvable"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@challenge_bp.route('/')
def index():
    return redirect(url_for('challenges.challenge_page'))
