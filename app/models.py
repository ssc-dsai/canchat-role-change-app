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
    Column("email", String),
    Column("role", String),
    Column("updated_at", BigInteger),
)