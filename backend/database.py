# backend/database.py

from sqlmodel import SQLModel, create_engine, Session
import os


DATABASE_URL = "sqlite:///./backend/database.db" 

# Creates an engine for SQLite
engine = create_engine(DATABASE_URL, echo=True)

# Function to get a session for interacting with the database
def get_session():
    return Session(engine)

def create_db_and_tables():
    # Check if the database folder exists
    if not os.path.exists('backend'):
        os.makedirs('backend')
    
    # Create tables
    SQLModel.metadata.create_all(engine)

create_db_and_tables()
