from flask import Flask, request, jsonify, session
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from helpers import hash_password
from sqlalchemy import func
from flask_session import Session
from flask_migrate import Migrate
import nltk
db = SQLAlchemy()
app = Flask(__name__)
nltk.download('punkt_tab')
app.config['SECRET_KEY'] = 'my_music_app1124'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:maaz_2412@localhost/music_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db


db.init_app(app)
Session(app)
migrate = Migrate(app, db)
MOOD_KEYWORDS = {
    "happy": ["happy", "joyful", "excited", "cheerful"],
    "sad": ["sad", "down", "depressed", "blue"],
    "energetic": ["energetic", "active", "motivated", "lively"]
}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
class SongCategories(db.Model):
    __tablename__ = 'song_categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(250), nullable=False)
class SongRecommendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('song_categories.category_id'), nullable=False)
    category_type = db.Column(db.String(100), nullable=False)
    song_name = db.Column(db.String(100), nullable=False)
@app.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"Error": "All fields are required"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"Error": "username already taken"}), 400
    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"Success": "User signup was successful"}), 201
@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"Error": "All fields are required"}), 400
        
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Invalid username or password"}), 400

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        session['username'] = user.username
        session['password'] = user.password
        return jsonify({"Success": "Login was successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 400
    
@app.route("/logout", methods=['POST'])
def logout():
    # Clear the session
    session.clear()
    return jsonify({"success": "Logged out successfully"}), 200

@app.route("/input-mood", methods=['POST'])
def input_mood():
    data = request.get_json()
    sentence = data['sentence']
    if not sentence:
        return jsonify({"Error": "Please enter a valid sentence"}), 400
    tokens = nltk.word_tokenize(sentence.lower())
    detected_keywords = {}
    for word in tokens:
        for mood, keywords in MOOD_KEYWORDS.items():
            if word in keywords:
                if mood not in detected_keywords:
                    detected_keywords[mood] = []
                detected_keywords[mood].append(word)
    for key, words in detected_keywords.items():
        song_category = SongCategories.query.filter(func.lower(SongCategories.category) == key.lower()).first()
        song_recommendation = SongRecommendations.query.filter_by(category_type=song_category.category).all()
        song_names = [song.song_name for song in song_recommendation]



    
    if not detected_keywords:
        return jsonify({
            "message": "No mood-related keywords detected.",
            "sentence": sentence,
            "keywords": []
        }), 200

    return jsonify({
        "message": "Mood-related keywords detected.",
        "sentence": sentence,
        "keywords": detected_keywords,
        "song_category": song_category.category,
        "Song_recommendations": song_names
    }), 200
@app.route("/protected", methods=["GET"])
def protected():
    if "username" in session:  # Assume session["user_id"] is set at login
        return jsonify({"message": "Access granted", "username": session["username"]})
    return jsonify({"message": "Access denied"}), 401

@app.route('/get-session', methods=['GET'])
def get_session():
    if 'username' in session:
        return jsonify({'username': session['username']}), 200
    return jsonify({'error': 'No session data found'}), 401

if __name__ == '__main__':
    app.run(debug=True)