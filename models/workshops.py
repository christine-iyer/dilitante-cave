from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Workshop(Base):
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(100), nullable=False)
    date = Column(String(100), nullable=False) 
    instructors = Column(Text, nullable=True)  # Use Text to store JSON strings
    students = Column(Text, nullable=True) 
    description = Column(String(255), nullable=True)

    # def __repr__(self):
    #     return f"<Workshop(id={self.id}, subject={self.subject}, date={self.date})>"