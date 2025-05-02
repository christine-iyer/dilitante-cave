from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.students import Student
from models.schemas import StudentCreate
from models.database import get_db
import logging
import json

router = APIRouter()
logging.basicConfig(level=logging.INFO)
@router.post("/students/")


@router.post("/students/")
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    logging.info(f"Received student data: {student}")
    db_student = db.query(Student).filter(Student.name == student.name).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Student already exists")
    
    new_student = Student(
        name=student.name,
        reasons=json.dumps(student.reasons),  # Convert to JSON
        picture=student.picture,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": "Student created", "student": {"name": new_student.name, "reasons": new_student.reasons}}