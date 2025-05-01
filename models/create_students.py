from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.students import Student
from models.schemas import StudentCreate  # Import the Pydantic schema
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MySQL credentials from .env
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# SQLAlchemy setup
DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app initialization
app = FastAPI()

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to the Students API! Use /students/ to interact with the API."}

# Optional favicon route
@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available."}

# POST /students/ endpoint
@app.post("/students/")
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check if the student already exists
    db_student = db.query(Student).filter(Student.name == student.name).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Student already exists")
    
    # Add the new student to the database
    new_student = Student(
        name=student.name,
        city=student.city,
        state=student.state,
        available=student.available,
        credentials=student.credentials,
        services=student.services,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": "Student created", "student": {"name": new_student.name, "services": new_student.services}}