from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.students import Student
from models.schemas import StudentCreate, StudentResponse
from models.database import get_db
from typing import List
import logging
import json

# Initialize the router
router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)

# POST endpoint to create a new student
@router.post("/students/")
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    logging.info(f"Received student data: {student}")
    
    # Check if the student already exists
    db_student = db.query(Student).filter(Student.name == student.name).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Student already exists")
    
    # Create a new student record
    new_student = Student(
        name=student.name,
        reasons=json.dumps(student.reasons),  # Convert list to JSON string
        picture=student.picture,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return {"message": "Student created", "student": {"name": new_student.name, "reasons": json.loads(new_student.reasons)}}

# GET endpoint to retrieve all students
@router.get("/students/", response_model=List[StudentResponse])
async def get_students(db: Session = Depends(get_db)):
    # Query all students from the database
    students = db.query(Student).all()
    
    # Deserialize the `reasons` field for each student
    for student in students:
        if isinstance(student.reasons, str):  # If reasons is a string
            try:
                student.reasons = json.loads(student.reasons)  # Try to parse as JSON
            except json.JSONDecodeError:
                student.reasons = student.reasons.split(", ")  # Fallback: split by comma
        elif student.reasons is None:
            student.reasons = []  # Default to an empty list if reasons is None
    
    # Return the list of students
    return students

# GET endpoint to retrieve and modify a student by ID
@router.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    # Query the student by ID
    student = db.query(Student).filter(Student.id == student_id).first()
    
    # If the student does not exist, raise a 404 error
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Deserialize the `reasons` field
    if isinstance(student.reasons, str):  # If reasons is a string
        try:
            student.reasons = json.loads(student.reasons)  # Try to parse as JSON
        except json.JSONDecodeError:
            student.reasons = student.reasons.split(", ")  # Fallback: split by comma
    elif student.reasons is None:
        student.reasons = []  # Default to an empty list if reasons is None
    
    return student
# PUT endpoint to update a student by ID
@router.put("/students/{student_id}")
async def update_student(student_id: int, updated_data: dict, db: Session = Depends(get_db)):
    # Query the student by ID
    student = db.query(Student).filter(Student.id == student_id).first()
    
    # If the student does not exist, raise a 404 error
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Update the fields provided in the request body
    for key, value in updated_data.items():
        if hasattr(student, key):  # Check if the field exists in the model
            setattr(student, key, value)
    
    # Commit the changes to the database
    db.commit()
    db.refresh(student)
    
    return {"message": "Student updated successfully", "student": student}
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
    
    return {"message": "Student deleted"}
# Note: The above code assumes that the database connection and models are set up correctly.