from pydantic import BaseModel
from typing import List, Optional

class InstructorCreate(BaseModel):
    name: str   
    bio: List[str]  # Expecting a list of strings
    skills: Optional[List[str]] = None  # Expecting a list of strings
    
class InstructorResponse(BaseModel):
    id: int
    name: str
    bio: Optional[List[str]]  # JSON array
    skills: Optional[List[str]]  # JSON array
    

class InstructorUpdate(BaseModel):
    name: Optional[str]
    bio: Optional[str]
    skills: Optional[list]
   

    class Config:
        from_attributes = True