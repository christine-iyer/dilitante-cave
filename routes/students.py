from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.students import Student
from schemas.students import StudentCreate, StudentResponse, StudentUpdate
from models.database import get_db
from typing import List
import logging
import json

# Initialize the router
router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)

# POST endpoint to create a new student
@router.post("/students/", response_model=StudentResponse)
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    logging.info(f"Received student data: {student}")
    
    # Check if the student already exists
    db_student = db.query(Student).filter(Student.name == student.name).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Student already exists")
    
    # Create a new student record
    new_student = Student(
        name=student.name,
        reasons=json.dumps(student.reasons) if student.reasons else "[]",  # Serialize list to JSON string
        picture=student.picture,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    # Deserialize reasons for the response
    new_student.reasons = json.loads(new_student.reasons)
    return new_student

# GET endpoint to retrieve all students
@router.get("/students/", response_model=List[StudentResponse])
async def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    for student in students:
        if isinstance(student.reasons, str):  # If reasons is a JSON string
            try:
                student.reasons = json.loads(student.reasons)  # Deserialize JSON string
            except json.JSONDecodeError:
                student.reasons = []  # Default to an empty list if deserialization fails
    return students

# GET endpoint to retrieve a single student by ID
@router.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Deserialize reasons for the response
    if isinstance(student.reasons, str):  # If reasons is a JSON string
        try:
            student.reasons = json.loads(student.reasons)
        except json.JSONDecodeError:
            student.reasons = []  # Default to an empty list if deserialization fails
    return student

# PUT endpoint to update a student by ID
@router.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, updated_data: StudentUpdate, db: Session = Depends(get_db)):
    # Query the student by ID
    student = db.query(Student).filter(Student.id == student_id).first()
    
    # If the student does not exist, raise a 404 error
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Update the fields provided in the request body
    for key, value in updated_data.dict(exclude_unset=True).items():  # Use .dict() to convert to a dictionary
        if key == "reasons" and isinstance(value, list):  # Serialize reasons if it's a list
            value = json.dumps(value)
        if hasattr(student, key):  # Check if the field exists in the model
            setattr(student, key, value)
    
    # Commit the changes to the database
    db.commit()
    db.refresh(student)
    
    # Deserialize reasons for the response
    if isinstance(student.reasons, str):  # If reasons is a JSON string
        try:
            student.reasons = json.loads(student.reasons)
        except json.JSONDecodeError:
            student.reasons = []  # Default to an empty list if deserialization fails
    return student
# DELETE endpoint to delete a student by ID
@router.delete("/students/{student_id}")
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    # Query the student by ID
    db_student = db.query(Student).filter(Student.id == student_id).first()
    
    # If the student does not exist, raise a 404 error
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Delete the student from the database
    db.delete(db_student)
    db.commit()
    
    return {"message": "Student deleted successfully"}