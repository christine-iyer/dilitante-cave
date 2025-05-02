from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Workshop(Base):
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False)  # Use DateTime for proper date handling
    instructors = Column(String(255), nullable=True)  # Comma-separated
    students = Column(String(255), nullable=True)  # Comma-separated
    description = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Workshop(id={self.id}, subject={self.subject}, date={self.date})>"