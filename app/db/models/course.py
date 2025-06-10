from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .professor import professor_course

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), nullable=False, unique=True)
    title = Column(String(100), nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    semester = Column(String(10), nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    prerequisites = Column(Integer, ForeignKey('courses.id'), nullable=True)
    max_enrollment = Column(Integer, nullable=False)

    department = relationship('Department', back_populates='courses')
    professors = relationship('Professor', secondary=professor_course, back_populates='courses_taught')
    enrollments = relationship('Enrollment', back_populates='course')
    prerequisite = relationship('Course', remote_side=[id], uselist=False)