from flask import Flask, render_template
from flask_cors import CORS
from app.models.challenge import Challenge
from uuid import UUID
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



if __name__ == '__main__':
    app.run(port=5001, debug=True)
