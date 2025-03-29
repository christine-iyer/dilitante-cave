from pydantic import BaseModel
from typing import List

class Student(BaseModel):
    full_name: str
    reason: str