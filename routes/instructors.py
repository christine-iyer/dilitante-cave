from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import json

from schemas.instructors import InstructorCreate, InstructorResponse, InstructorUpdate
from models.database import get_db
from models.instructors import Instructor

# Initialize the router
router = APIRouter()

# POST endpoint to create a new instructor
@router.post("/instructors/", response_model=InstructorResponse)
async def create_instructor(instructor: InstructorCreate, db: Session = Depends(get_db)):
    # Serialize the skills field to JSON
    new_instructor = Instructor(
        name=instructor.name,
        skills=json.dumps(instructor.skills) if instructor.skills else "[]",  # Serialize list to JSON string
        bio=instructor.bio
    )
    db.add(new_instructor)
    db.commit()
    db.refresh(new_instructor)

    # Deserialize skills for the response
    new_instructor.skills = json.loads(new_instructor.skills)
    return new_instructor

# GET endpoint to retrieve all instructors
@router.get("/instructors/", response_model=List[InstructorResponse])
async def get_instructors(db: Session = Depends(get_db)):
    instructors = db.query(Instructor).all()
    for instructor in instructors:
        # Deserialize JSON strings back to Python lists
        if isinstance(instructor.skills, str):
            try:
                instructor.skills = json.loads(instructor.skills)
            except json.JSONDecodeError:
                instructor.skills = []  # Default to an empty list if deserialization fails
    return instructors

# GET endpoint to retrieve a single instructor by ID
@router.get("/instructors/{instructor_id}", response_model=InstructorResponse)
async def get_instructor(instructor_id: int, db: Session = Depends(get_db)):
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

    # Deserialize JSON strings back to Python lists
    if isinstance(instructor.skills, str):
        try:
            instructor.skills = json.loads(instructor.skills)
        except json.JSONDecodeError:
            instructor.skills = []  # Default to an empty list if deserialization fails
    return instructor

# PUT endpoint to update an instructor by ID
@router.put("/instructors/{instructor_id}", response_model=InstructorResponse)
async def update_instructor(instructor_id: int, updated_data: InstructorUpdate, db: Session = Depends(get_db)):
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

    # Update only the fields provided in the request body
    update_data = updated_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "skills" and isinstance(value, list):  # Serialize skills if it's a list
            value = json.dumps(value)
        setattr(instructor, key, value)

    db.commit()
    db.refresh(instructor)

    # Deserialize skills for the response
    if isinstance(instructor.skills, str):
        try:
            instructor.skills = json.loads(instructor.skills)
        except json.JSONDecodeError:
            instructor.skills = []  # Default to an empty list if deserialization fails
    return instructor

# DELETE endpoint to delete an instructor by ID
@router.delete("/instructors/{instructor_id}")
async def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

    db.delete(instructor)
    db.commit()
    return {"message": "Instructor deleted successfully"}