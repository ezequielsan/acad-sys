from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from .base import Base

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    birth_date = Column(Date, nullable=False)
    enrollment_date = Column(Date, nullable=False)
    major = Column(String(100), nullable=True)
    enrollment_number = Column(Integer, nullable=False, unique=True)

    enrollments = relationship('Enrollment', back_populates='student')