import logging
import os
import re
from dotenv import load_dotenv


# Load .env file
load_dotenv()

log = logging.getLogger(__name__)



def setup_logging():
    ACCESS_LOG_NAME: str = "uvicorn.access"

    class HealthCheckLoggingFilter(logging.Filter):
        def filter(self, record):
            # Here we match the log message's route or path for `/health` and `/health/db`.
            return not ("/health" in record.getMessage())

    health_check_filter = HealthCheckLoggingFilter()

    uvicorn_access_logger = logging.getLogger(ACCESS_LOG_NAME)
    uvicorn_access_logger.addFilter(health_check_filter)

def validate_prefix(prefix: str) -> str:
    if not prefix:
        return ""
    
    # Normalize
    prefix = "/" + prefix.strip("/")

    log.info(f"Validating API prefix: {prefix}")
    
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