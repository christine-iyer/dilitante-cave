from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Workshop(Base):
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(100), nullable=False)
    date: Column(String, nullable=False)
    instructors = Column(String(255), nullable=True)  # Comma-separated
    students = Column(String(255), nullable=True)  # Comma-separated
    description = Column(String(255), nullable=True)  # Comma-separated
   