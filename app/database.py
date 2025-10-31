from databases import Database
from sqlalchemy import create_engine, MetaData

from app.config import DATABASE_URL
import os

# Database connection
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Include this function to create all tables automatically on startup
def create_tables():
    metadata.create_all(bind=engine, checkfirst=True)