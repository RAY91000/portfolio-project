from flask import Flask, render_template
from flask_cors import CORS
from app.models.challenge import Challenge
from uuid import UUID
from flask_jwt_extended import verify_jwt_in_request
from app.extensions import db

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5001"}}, supports_credentials=True)




@app.route('/')
def landing():
    return render_template('landing.html')
    
@app.route('/home')
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

@app.route('/start.html/<uuid:id>')
def start_challenge(id):
    return render_template('start.html')

@app.route('/verify_email')
def verify_email():
    return render_template('verify_email.html')



@app.after_request
def add_cors_headers(response):
            response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5001"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            return response

if __name__ == '__main__':
    app.run(port=5001, debug=True)
