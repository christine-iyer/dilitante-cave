from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    bio = Column(String(255), nullable=True)  # Comma-separated
    skills = Column(String(255), nullable=True)  # Comma-separated