from pydantic import BaseModel
from typing import List, Optional

class InstructorBase(BaseModel):
    name: str
    skills: Optional[List[str]] = None  # JSON list
    bio: Optional[str] = None
    

class InstructorCreate(InstructorBase):
    pass

class InstructorResponse(InstructorBase):
    id: int

    class Config:
        from_attributes = True  # For SQLAlchemy model compatibility

# Add this class for updates
class InstructorUpdate(BaseModel):
    name: Optional[str] = None
    skills: Optional[List[str]] = None  # JSON list
    bio: Optional[str] = None