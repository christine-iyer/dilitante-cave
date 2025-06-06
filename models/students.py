from sqlalchemy import Column, String, Integer, JSON 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    reasons = Column(JSON(255), nullable=True)  # Comma-separated
    picture = Column(String(255), nullable=True)  # Comma-separated