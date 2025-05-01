from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    name: str
    city: str
    state: str
    available: Optional[bool] = True
    credentials: Optional[str] = None
    services: Optional[str] = None