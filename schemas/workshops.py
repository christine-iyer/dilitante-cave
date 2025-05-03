from pydantic import BaseModel
from typing import List, Optional

class WorkshopBase(BaseModel):
    subject: str
    date: str
    instructors: Optional[List[str]] = None  # Correctly named "instructors"
    students: Optional[List[str]] = None
    description: Optional[str] = None

class WorkshopCreate(WorkshopBase):
    pass

class WorkshopResponse(WorkshopBase):
    id: int

    class Config:
        orm_mode = True  # For Pydantic v2
   
class WorkshopResponse(BaseModel):
    id: int
    subject: Optional[List[str]]  # JSON array
    instructors: Optional[List[str]]  # JSON array
    students: Optional[List[str]]  # JSON array
    description: Optional[str]  # JSON array
    
class WorkshopUpdate(BaseModel):
    subject: Optional[List[str]]  # JSON array
    instructors: Optional[List[str]]  # JSON array
    students: Optional[List[str]]  # JSON array
    description: Optional[str]  # JSON array
   

    class Config:
        from_attributes = True