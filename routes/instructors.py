from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas.instructors import InstructorCreate, InstructorResponse, InstructorUpdate
from models.database import get_db
from typing import List
import logging
import json
from models.instructors import Instructor

# Initialize the router
router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)

# POST endpoint to create a new instructor
@router.post("/instructors/", response_model=InstructorResponse)
async def create_instructor(instructor: InstructorCreate, db: Session = Depends(get_db)):
    new_instructor = Instructor(
        name=instructor.name,
        skills=json.dumps(instructor.skills),  # Serialize list to JSON string
        bio=instructor.bio,
    )
    db.add(new_instructor)
    db.commit()
    db.refresh(new_instructor)
    # Deserialize JSON strings back to Python lists for the response
    new_instructor.skills = json.loads(new_instructor.skills)

    return new_instructor

# GET endpoint to retrieve all instructors
@router.get("/instructors/", response_model=List[InstructorResponse])
async def get_instructors(db: Session = Depends(get_db)):
    instructors = db.query(Instructor).all()
    for instructor in instructors:
        # Safely deserialize JSON strings back to Python lists
        try:
            instructor.skills = json.loads(instructor.skills) if instructor.skills else []
        except json.JSONDecodeError:
            instructor.skills = []  # Default to an empty list if deserialization fails

    return instructors

# GET endpoint to retrieve and modify a instructor by ID
@router.get("/instructors/{instructor_id}", response_model=InstructorResponse)
async def get_instructor(instructor_id: int, db: Session = Depends(get_db)):
    # Query the instructor by ID
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    
    # If the instructor does not exist, raise a 404 error
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    # Deserialize the `bio` field
    if isinstance(instructor.bio, str):  # If bio is a string
        try:
            instructor.bio = json.loads(instructor.bio)  # Try to parse as JSON
        except json.JSONDecodeError:
            instructor.bio = instructor.bio.split(", ")  # Fallback: split by comma
    elif instructor.bio is None:
        instructor.bio = []  # Default to an empty list if bio is None
    return instructor
# PUT endpoint to update a instructor by ID
@router.put("/instructors/{instructor_id}", response_model=InstructorResponse)
async def update_instructor(instructor_id: int, updated_data: InstructorUpdate, db: Session = Depends(get_db)):
    # Query the instructor by ID
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    
    # If the instructor does not exist, raise a 404 error
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    # Update the fields provided in the request body
    update_data = updated_data.dict(exclude_unset=True)  # Only include fields that are set
    for key, value in update_data.items():
        setattr(instructor, key, value)
    
    # Commit the changes to the database
    db.commit()
    db.refresh(instructor)
    
    return instructor
# DELETE endpoint to delete a instructor by ID
@router.delete("/instructors/{instructor_id}")    
async def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    # Query the instructor by ID
    db_instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    
    # If the instructor does not exist, raise a 404 error
    if not db_instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    # Delete the instructor from the database
    db.delete(db_instructor)
    db.commit()
    
    return {"message": "Instructor deleted"}
# Note: The above code assumes that the database connection and models are set up correctly.