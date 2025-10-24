from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
APP_NAME = os.getenv("APP_NAME", "CANChat Role Management App")
APP_ENV = os.getenv("APP_ENV", "production")
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", ['*'])
ALLOWED_EMAILS = os.getenv("ALLOWED_EMAILS", "").split(",")
ALLOWED_ROLES = os.getenv("ALLOWED_ROLES", "").split(",")

# Build base Database URL
base_url = (
    f"postgresql://"
    f"{os.getenv('POSTGRES_USER', 'user')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'password')}@"
    f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
    f"{os.getenv('POSTGRES_PORT', '5432')}/"
    f"{os.getenv('POSTGRES_NAME', 'postgres')}"
)

# Add SSL parameters
ssl_mode = os.getenv('POSTGRES_SSLMODE', 'verify-full')
base_url += f"?sslmode={ssl_mode}"

if ssl_mode in ['verify-full', 'verify-ca']:
    ssl_cert = os.getenv('POSTGRES_SSLROOTCERT', '/etc/ssl/certs/ca.crt')
    base_url += f"&sslrootcert={ssl_cert}"

DATABASE_URL = base_url