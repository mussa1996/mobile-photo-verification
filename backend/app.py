# backend/app.py
import os
import logging
from flask import Flask, request, jsonify
from config import DEBUG, UPLOAD_FOLDER
from database import db, User
from auth import generate_token, verify_token
from utils import check_photo_author

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    
    # Initialize SQLAlchemy
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data or 'signature' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        username = data['username']
        password = data['password']
        signature = data['signature']
        
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "User already exists"}), 400
        
        user = User(username=username, signature=signature)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        logger.info("User registered: %s", username)
        return jsonify({"message": "User registered successfully"}), 201
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Missing username or password"}), 400
        
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            token = generate_token(user.id)
            return jsonify({"token": token})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    
    @app.route('/upload', methods=['POST'])
    def upload():
        # Retrieve JWT token from the Authorization header
        auth_header = request.headers.get('Authorization', '')
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        if not token:
            return jsonify({"error": "Missing token"}), 401
        
        user_id = verify_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Retrieve user from database
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if 'photo' not in request.files:
            return jsonify({"error": "No photo provided"}), 400
        
        file = request.files['photo']
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400
        
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        logger.info("File saved: %s", file_path)
        
        # Verify the photo metadata against the expected signature
        verified = check_photo_author(file_path, user.signature)
        if verified:
            return jsonify({"result": "Photo confirmed to be taken by you."})
        else:
            return jsonify({"result": "Photo not recognized as taken by you."})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=DEBUG)
