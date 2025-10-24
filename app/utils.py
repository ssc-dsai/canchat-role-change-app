from app.config import ALLOWED_EMAILS, ALLOWED_ROLES

# Check if a user is authorized to perform role changes
def is_authorized(user_email: str) -> bool:
    return user_email in ALLOWED_EMAILS

# Validate new role (based on your business rules)
def is_valid_role(role: str) -> bool:
    return role in ALLOWED_ROLES