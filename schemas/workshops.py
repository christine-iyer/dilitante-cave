from pydantic import BaseModel
from typing import List, Optional

class WorkshopBase(BaseModel):
    subject: str
    date: str  # Store the formatted date as a string
    instructors: Optional[List[str]] = None  # JSON list
    students: Optional[List[str]] = None  # JSON list
    description: Optional[str] = None

class WorkshopCreate(WorkshopBase):
    pass

class WorkshopResponse(WorkshopBase):
    id: int

    class Config:
        from_attributes = True  # For SQLAlchemy model compatibility

# Add this class for updates
class WorkshopUpdate(BaseModel):
    subject: Optional[str] = None
    date: Optional[str] = None
    instructors: Optional[List[str]] = None
    students: Optional[List[str]] = None
    description: Optional[str] = None