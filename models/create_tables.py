from sqlalchemy import create_engine
from models.student import Student
from models.instructor import Instructor
from models.workshop import Workshop
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing!")

# Set up SQLAlchemy engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()