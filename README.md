# mobile-photo-verification

Photo Verification System with Flask and Kivy This project is an end-to-end example of a photo verification system that uses Python for both the backend (Flask) and mobile frontend (Kivy).
Users can upload a photo, and the server verifies whether the photo was taken by them based on metadata (e.g., checking the EXIF "Artist" tag). The system is designed to be modular and extensible, with features like user registration, secure authentication (JWT), and a SQLite database (SQLAlchemy).

# Key Features

# Backend (Flask):

User registration and secure authentication using JWT.

Photo upload and metadata verification (using Pillow and piexif).

SQLite database for storing user and photo data.

Enhanced logging and error handling.

# Frontend (Kivy):

Mobile interface for uploading photos and viewing verification results.

# Extensible Design:

Modular code structure for easy extension (e.g., adding watermarks or custom metadata like "zxif").

Customizable verification logic.

# Technologies Used
# Backend: Flask, SQLAlchemy, JWT, Pillow, piexif.

# Frontend: Kivy.

# Database: SQLite.

# How It Works
Users register and log in via the mobile app.

They upload a photo, which is sent to the Flask backend.

The server verifies the photo's metadata (e.g., EXIF "Artist" tag) to confirm ownership.

The verification result is sent back to the mobile app.

# Future Improvements
Add watermarking to photos for additional verification.

Support for custom metadata tags (e.g., "zxif").

Enhance the mobile UI/UX.
