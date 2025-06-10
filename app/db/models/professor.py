from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base

# Tabela associativa para N:N entre Professor e Course
professor_course = Table(
    'professor_course', Base.metadata,
    Column('professor_id', Integer, ForeignKey('professors.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

class Professor(Base):
    __tablename__ = 'professors'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    hire_date = Column(Date, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    title = Column(String(50), nullable=True)

    department = relationship('Department', back_populates='professors', foreign_keys=[department_id])
    courses_taught = relationship('Course', secondary=professor_course, back_populates='professors')

