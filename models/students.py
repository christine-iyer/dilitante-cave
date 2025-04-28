# from pydantic import BaseModel
# from typing import List

# class Student(BaseModel):
#     full_name: str
#     reason: str
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    full_name = Column(String, primary_key=True, index=True)
    reason = Column(String)