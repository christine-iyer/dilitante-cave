from pydantic import BaseModel
from typing import List, Optional

class WorkshopCreate(BaseModel):
    date: str   
    subject: str
    instrctors: List[str]  # Expecting a list of strings
    students: List[str]  # Expecting a list of strings
    description: str
   
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