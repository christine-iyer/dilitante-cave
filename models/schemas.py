from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    name: str
    reasons: Optional[str] = None
    picture: str