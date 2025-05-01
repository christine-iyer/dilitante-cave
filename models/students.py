<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

=======
# from pydantic import BaseModel
# from typing import List

# class Student(BaseModel):
#     full_name: str
#     reason: str
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

>>>>>>> e98a466f56a0030b5a942435b0dd439cfed58bbb
Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
<<<<<<< HEAD

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    available = Column(Boolean, default=True)
    credentials = Column(String(255), nullable=True)  # Comma-separated
    services = Column(String(255), nullable=True)  # Comma-separated# from pydantic import BaseModel
# from typing import List

# class Student(BaseModel):
#     full_name: str
#     reason: str
=======
    full_name = Column(String, primary_key=True, index=True)
    reason = Column(String)
>>>>>>> e98a466f56a0030b5a942435b0dd439cfed58bbb
