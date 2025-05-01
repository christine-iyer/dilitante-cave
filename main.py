# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List
# import pymongo
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# MONGO_URI = os.getenv("MONGO_URI")
# if not MONGO_URI:
#     raise ValueError("❌ MONGO_URI is missing!")

# client = pymongo.MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
# db = client["codebar"]
# workshops_collection = db["workshops"]
# students_collection = db["students"]
# instructors_collection = db["instructors"]

# class Student(BaseModel):
#     full_name: str
#     reason: str

# class Instructor(BaseModel):
#     full_name: str
#     bio: str
#     skills: List[str] = []

# class Workshop(BaseModel):
#     date: str
#     subject: str
#     students: List[str] = []
#     instructors: List[str] = []

# @app.post("/students/")
# async def create_student(student: Student):
#     students_collection.insert_one(student.dict())
#     return {"message": "Student created"}

# @app.get("/students/")
# async def get_students():
#     return list(students_collection.find({}, {"_id": 0}))

# @app.put("/students/{full_name}")
# async def update_student(full_name: str, student: Student):
#     result = students_collection.update_one(
#         {"full_name": full_name},
#         {"$set": student.dict()}
#     )
#     if result.matched_count == 0:
#         raise HTTPException(status_code=404, detail="Student not found")
#     return {"message": "Student updated"}

# @app.post("/instructors/")
# async def create_instructor(instructor: Instructor):
#     instructors_collection.insert_one(instructor.dict())
#     return {"message": "Instructor created"}

# @app.get("/instructors/")
# async def get_instructors():
#     return list(instructors_collection.find({}, {"_id": 0}))

# @app.put("/instructors/{full_name}")
# async def update_instructor(full_name: str, instructor: Instructor):
#     result = instructors_collection.update_one(
#         {"full_name": full_name},
#         {"$set": instructor.dict()}
#     )
#     if result.matched_count == 0:
#         raise HTTPException(status_code=404, detail="Instructor not found")
#     return {"message": "Instructor information updated"}

# @app.post("/workshops/")
# async def create_workshop(workshop: Workshop):
#     if workshops_collection.find_one({"subject": workshop.subject}):
#         raise HTTPException(status_code=400, detail="Workshop already exists")
#     workshops_collection.insert_one(workshop.dict())
#     return {"message": "Workshop created"}

# @app.get("/workshops/")
# async def get_workshops():
#     return list(workshops_collection.find({}, {"_id": 0}))

# @app.put("/workshops/{subject}")
# async def update_workshop(subject: str, updated_workshop: Workshop):
#     result = workshops_collection.update_one(
#         {"subject": subject},
#         {"$set": updated_workshop.dict()}
#     )
#     if result.matched_count == 0:
#         raise HTTPException(status_code=404, detail="Workshop not found")
#     return {"message": "Workshop updated"}
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing!")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app initialization
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Student model
class Student(Base):
    __tablename__ = "students"
    full_name = Column(String, primary_key=True, index=True)
    reason = Column(String)

# Create database tables
Base.metadata.create_all(bind=engine)

# POST /students/ endpoint
@app.post("/students/")
async def create_student(student: Student, db: Session = Depends(get_db)):
    # Check if the student already exists
    db_student = db.query(Student).filter(Student.full_name == student.full_name).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Student already exists")
    
    # Add the new student to the database
    db.add(student)
    db.commit()
    db.refresh(student)
    return {"message": "Student created", "student": {"full_name": student.full_name, "reason": student.reason}}
