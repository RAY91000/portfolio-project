from flask import Flask, render_template
from flask_cors import CORS
from app.models.challenge import Challenge
from uuid import UUID
from flask_jwt_extended import verify_jwt_in_request
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/challenges')
def challenges():
    return render_template('challenges.html')

@app.route('/challenge/<uuid:id>')
def challenge_detail(id):
    return render_template("challenge_detail.html")

@app.route('/profile')
def profile():
    try:
        verify_jwt_in_request()
    except Exception as e:
        print(f"JWT verification failed: {e}")
    return render_template('profile.html')

@app.route("/profile/settings")
def profile_settings():
    return render_template("settings.html")


if __name__ == '__main__':
    app.run(port=5001, debug=True)
