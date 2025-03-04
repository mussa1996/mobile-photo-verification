# backend/config.py
import os

# Flask configuration
DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")

# JWT configuration
JWT_SECRET = os.environ.get("JWT_SECRET", "your-jwt-secret")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600  # Token valid for 1 hour

# Database configuration (using SQLite for simplicity)
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Upload folder for saving photos
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
