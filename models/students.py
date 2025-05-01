from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    available = Column(Boolean, default=True)
    credentials = Column(String(255), nullable=True)  # Comma-separated
    services = Column(String(255), nullable=True)  # Comma-separated