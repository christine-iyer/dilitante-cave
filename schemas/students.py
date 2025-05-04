from pydantic import BaseModel
from typing import List, Optional

class StudentCreate(BaseModel):
    name: str   
    reasons: Optional[List[str]] = None  # Expecting a list of strings
    picture: Optional[str] = None   

class StudentResponse(BaseModel):
    id: int
    name: str
    reasons: Optional[List[str]]  # JSON array
    picture: Optional[str]  

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    reasons: Optional[List[str]] = None  # Use List[str] for consistency
    picture: Optional[str] = None

    class Config:
        from_attributes = True