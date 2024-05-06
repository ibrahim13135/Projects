from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///chat_app.db")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

      # Configure JWT to use cookies
    JWT_TOKEN_LOCATION = ["cookies"]  # JWTs will be read from cookies
    JWT_COOKIE_SECURE = True  # Only send cookies over HTTPS
    JWT_COOKIE_CSRF_PROTECT = False  # Set to True if you need CSRF protection
    JWT_ACCESS_COOKIE_NAME = "access_token"  # Cookie name for the JWT access token
    JWT_COOKIE_SAMESITE = "Lax"  # Controls cross-site cookie behavior
