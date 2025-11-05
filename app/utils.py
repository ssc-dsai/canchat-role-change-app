from app.config import ALLOWED_ROLES

# Validate new role (based on your business rules)
def is_valid_role(role: str) -> bool:
    return role in ALLOWED_ROLES