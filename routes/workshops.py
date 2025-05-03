from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.workshops import Workshop
from schemas.workshops import WorkshopCreate, WorkshopResponse, WorkshopUpdate
from models.database import get_db
from typing import List
import logging
import json

# Initialize the router
router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)

# POST endpoint to create a new workshop
@router.post("/workshops/", response_model=WorkshopResponse)
async def create_workshop(workshop: WorkshopCreate, db: Session = Depends(get_db)):
    new_workshop = Workshop(
        subject=workshop.subject,
        date=workshop.date,
        instructors=",".join(workshop.instructors) if workshop.instructors else None,
        students=",".join(workshop.students) if workshop.students else None,
        description=workshop.description,
    )
    db.add(new_workshop)
    db.commit()
    db.refresh(new_workshop)
    return new_workshop

# GET endpoint to retrieve all workshops
@router.get("/workshops/", response_model=List[WorkshopResponse])
async def get_workshops(db: Session = Depends(get_db)):
    workshops = db.query(Workshop).all()
    for workshop in workshops:
        # Convert comma-separated strings back to lists
        workshop.instructors = workshop.instructors.split(",") if workshop.instructors else []
        workshop.students = workshop.students.split(",") if workshop.students else []
    return workshops

# GET endpoint to retrieve and modify a workshop by ID
@router.get("/workshops/{workshop_id}", response_model=WorkshopResponse)
async def get_workshop(workshop_id: int, db: Session = Depends(get_db)):
    # Query the workshop by ID
    workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    
    # If the workshop does not exist, raise a 404 error
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    
    # Deserialize the `description` field
    if isinstance(workshop.description, str):  # If description is a string
        try:
            workshop.description = json.loads(workshop.description)  # Try to parse as JSON
        except json.JSONDecodeError:
            workshop.description = workshop.description.split(", ")  # Fallback: split by comma
    elif workshop.description is None:
        workshop.description = []  # Default to an empty list if description is None
    
    return workshop
# PUT endpoint to update a workshop by ID
@router.put("/workshops/{workshop_id}")
async def update_workshop(workshop_id: int, updated_data: WorkshopUpdate, db: Session = Depends(get_db)):
    # Query the workshop by ID
    workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    
    # If the workshop does not exist, raise a 404 error
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    
    # Update the fields provided in the request body
    for key, value in updated_data.items():
        if hasattr(workshop, key):  # Check if the field exists in the model
            setattr(workshop, key, value)
    
    # Commit the changes to the database
    db.commit()
    db.refresh(workshop)
    
    return {"message": "Workshop updated successfully", "workshop": workshop}
# DELETE endpoint to delete a workshop by ID
@router.delete("/workshops/{workshop_id}")    
async def delete_workshop(workshop_id: int, db: Session = Depends(get_db)):
    # Query the workshop by ID
    db_workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    
    # If the workshop does not exist, raise a 404 error
    if not db_workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    
    # Delete the workshop from the database
    db.delete(db_workshop)
    db.commit()
    
    return {"message": "Workshop deleted"}
# Note: The above code assumes that the database connection and models are set up correctly.