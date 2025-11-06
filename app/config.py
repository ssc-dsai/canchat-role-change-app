import os
import re
from dotenv import load_dotenv


# Load .env file
load_dotenv()


def validate_prefix(prefix: str) -> str:
    if not prefix:
        return ""
    
    # Normalize
    prefix = "/" + prefix.strip("/")

    print(f"Validating API prefix: {prefix}")
    
    # Allow single "/"
    if prefix == "/":
        return prefix
    
    # No trailing slash allowed
    prefix = prefix.rstrip("/")

    # RFC 3986 valid path characters:
    # ALPHA / DIGIT / "-" / "." / "_" / "~" / "%" / "/" allowed
    # but we'll disallow spaces, ?, #, and ensure structure
    PATH_REGEX = re.compile(r"^/([A-Za-z0-9\-\._~%]+(/)?)*$")
    
    if not PATH_REGEX.match(prefix):
        raise ValueError(f"Invalid path prefix: {prefix}")

    return prefix

def validate_db_url(db_url: str) -> str:
    if not db_url:
        raise ValueError("DATABASE_URL is required")
    
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    # Basic validation for common schemes
    DB_URL_REGEX = re.compile(r"^(postgresql|mysql|sqlite)://[^\s]+$")
    
    if not DB_URL_REGEX.match(db_url):
        raise ValueError(f"Invalid DATABASE_URL: {db_url}")
    
    return db_url

APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
APP_NAME = os.getenv("APP_NAME", "CANChat Role Management App")
APP_NAME_FR = os.getenv("APP_NAME_FR", "Application de gestion des rôles CANChat")
APP_ENV = os.getenv("APP_ENV", "production")
APP_PREFIX = validate_prefix(os.getenv("APP_PREFIX", ""))
API_PREFIX = validate_prefix(os.getenv("API_PREFIX", "/api/v1"))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", ['*'])
EMAIL_HEADER_NAME = os.getenv("EMAIL_HEADER_NAME", "X-Forwarded-Email")

DATABASE_URL = validate_db_url(os.getenv("DATABASE_URL"))
ALLOWED_ROLES = os.getenv("ALLOWED_ROLES", "").split(",")