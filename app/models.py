import time
from pydantic import BaseModel, EmailStr
from sqlalchemy import Table, Column, String, BigInteger
from app.database import metadata

# Response messages
class RoleChangeRequest(BaseModel):
    role: str
class RoleResponse(BaseModel):
    email: EmailStr
    role: str

# Table definition for user roles
user = Table(
    "user",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String),
    Column("email", String, unique=True, nullable=False),   # Unique email for each user
    Column("role", String, nullable=False), # Role (user, admin, etc.)
    Column("domain", String),
    Column("created_at", BigInteger, server_default=int(time.time())),
    Column("updated_at", BigInteger, server_default=int(time.time()), onupdate=int(time.time())),
)