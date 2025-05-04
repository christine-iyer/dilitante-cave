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
        date=workshop.date,  # Store the formatted date as a string
        instructors=json.dumps(workshop.instructors),  # Serialize list to JSON string
        students=json.dumps(workshop.students),  # Serialize list to JSON string
        description=workshop.description,
    )
    db.add(new_workshop)
    db.commit()
    db.refresh(new_workshop)
    # Deserialize JSON strings back to Python lists for the response
    new_workshop.instructors = json.loads(new_workshop.instructors)
    new_workshop.students = json.loads(new_workshop.students)

    return new_workshop

# GET endpoint to retrieve all workshops
@router.get("/workshops/", response_model=List[WorkshopResponse])
async def get_workshops(db: Session = Depends(get_db)):
    workshops = db.query(Workshop).all()
    for workshop in workshops:
        # Deserialize JSON strings back to Python lists
        if isinstance(workshop.instructors, str):  # If instructors is a JSON string
            try:
                workshop.instructors = json.loads(workshop.instructors)
            except json.JSONDecodeError:
                workshop.instructors = []  # Default to an empty list if deserialization fails

        if isinstance(workshop.students, str):  # If students is a JSON string
            try:
                workshop.students = json.loads(workshop.students)
            except json.JSONDecodeError:
                workshop.students = []  # Default to an empty list if deserialization fails

    return workshops

# GET endpoint to retrieve a single workshop by ID
@router.get("/workshops/{workshop_id}", response_model=WorkshopResponse)
async def get_workshop(workshop_id: int, db: Session = Depends(get_db)):
    workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")

    # Deserialize JSON strings back to Python lists
    if isinstance(workshop.instructors, str):  # If instructors is a JSON string
        try:
            workshop.instructors = json.loads(workshop.instructors)
        except json.JSONDecodeError:
            workshop.instructors = []  # Default to an empty list if deserialization fails

    if isinstance(workshop.students, str):  # If students is a JSON string
        try:
            workshop.students = json.loads(workshop.students)
        except json.JSONDecodeError:
            workshop.students = []  # Default to an empty list if deserialization fails

    return workshop


# PUT endpoint to update a workshop by ID
@router.put("/workshops/{workshop_id}", response_model=WorkshopResponse)
async def update_workshop(workshop_id: int, updated_data: WorkshopUpdate, db: Session = Depends(get_db)):
    # Query the workshop by ID
    workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    
    # If the workshop does not exist, raise a 404 error
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    
    # Update the fields provided in the request body
    update_data = updated_data.dict(exclude_unset=True)  # Only include fields that are set
    for key, value in update_data.items():
        if key == "instructors" and isinstance(value, list):  # Serialize instructors if it's a list
            value = json.dumps(value)
        if key == "students" and isinstance(value, list):  # Serialize students if it's a list
            value = json.dumps(value)
        setattr(workshop, key, value)
    
    # Commit the changes to the database
    db.commit()
    db.refresh(workshop)
    
    # Deserialize JSON fields for the response
    if isinstance(workshop.instructors, str):  # If instructors is a JSON string
        try:
            workshop.instructors = json.loads(workshop.instructors)
        except json.JSONDecodeError:
            workshop.instructors = []  # Default to an empty list if deserialization fails

    if isinstance(workshop.students, str):  # If students is a JSON string
        try:
            workshop.students = json.loads(workshop.students)
        except json.JSONDecodeError:
            workshop.students = []  # Default to an empty list if deserialization fails

    return workshop

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