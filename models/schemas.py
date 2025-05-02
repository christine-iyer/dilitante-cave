from pydantic import BaseModel
from typing import List, Optional

class StudentCreate(BaseModel):
    name: str   
    reasons: List[str]  # Expecting a list of strings
    picture: Optional[str] = None   

class StudentResponse(BaseModel):
    id: int
    name: str
    reasons: Optional[List[str]]  # JSON array
    picture: Optional[str]    

    class Config:
        from_attributes = True