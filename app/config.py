from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
APP_NAME = os.getenv("APP_NAME", "CANChat Role Management App")
APP_ENV = os.getenv("APP_ENV", "production")
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", ['*'])

DATABASE_URL = os.getenv("DATABASE_URL")
ALLOWED_EMAILS = os.getenv("ALLOWED_EMAILS", "").split(",")
ALLOWED_ROLES = os.getenv("ALLOWED_ROLES", "").split(",")