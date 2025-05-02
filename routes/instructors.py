from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.instructors import Instructor
from schemas.instructors import InstructorCreate, InstructorResponse, InstructorUpdate
from models.database import get_db
from typing import List
import logging
import json

# Initialize the router
router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)

# POST endpoint to create a new instructor
@router.post("/instructors/")
async def create_instructor(instructor: InstructorCreate, db: Session = Depends(get_db)):
    logging.info(f"Received instructor data: {instructor}")
    
    # Check if the instructor already exists
    db_instructor = db.query(Instructor).filter(Instructor.name == instructor.name).first()
    if db_instructor:
        raise HTTPException(status_code=400, detail="Instructor already exists")
    
    # Create a new instructor record
    new_instructor = Instructor(
        name=instructor.name,
        skills=json.dumps(instructor.skills),  # Convert list to JSON string
        bio=instructor.bio,
    )
    db.add(new_instructor)
    db.commit()
    db.refresh(new_instructor)
    
    return {"message": "Instructor created", "instructor": {"name": new_instructor.name, "skills": json.loads(new_instructor.skills)}}

# GET endpoint to retrieve all instructors
@router.get("/instructors/", response_model=List[InstructorResponse])
async def get_instructors(db: Session = Depends(get_db)):
    # Query all instructors from the database
    instructors = db.query(Instructor).all()
    
    # Deserialize the `skills` field for each instructor
    for instructor in instructors:
        if isinstance(instructor.skills, str):  # If skills is a string
            try:
                instructor.skills = json.loads(instructor.skills)  # Try to parse as JSON
            except json.JSONDecodeError:
                instructor.skills = instructor.skills.split(", ")  # Fallback: split by comma
        elif instructor.skills is None:
            instructor.skills = []  # Default to an empty list if skills is None
    
    # Return the list of instructors
    return instructors

# GET endpoint to retrieve and modify a instructor by ID
@router.get("/instructors/{instructor_id}", response_model=InstructorResponse)
async def get_instructor(instructor_id: int, db: Session = Depends(get_db)):
    # Query the instructor by ID
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    
    # If the instructor does not exist, raise a 404 error
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    # Deserialize the `skills` field
    if isinstance(instructor.skills, str):  # If skills is a string
        try:
            instructor.skills = json.loads(instructor.skills)  # Try to parse as JSON
        except json.JSONDecodeError:
            instructor.skills = instructor.skills.split(", ")  # Fallback: split by comma
    elif instructor.skills is None:
        instructor.skills = []  # Default to an empty list if skills is None
    
    return instructor
# PUT endpoint to update a instructor by ID
@router.put("/instructors/{instructor_id}")
async def update_instructor(instructor_id: int, updated_data: InstructorUpdate, db: Session = Depends(get_db)):
    # Query the instructor by ID
    instructor = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    
    # If the instructor does not exist, raise a 404 error
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    # Update the fields provided in the request body
    for key, value in updated_data.items():
        if hasattr(instructor, key):  # Check if the field exists in the model
            setattr(instructor, key, value)
    
    # Commit the changes to the database
    db.commit()
    db.refresh(instructor)
    
    return {"message": "Instructor updated successfully", "instructor": instructor}
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