from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    head_id = Column(Integer, ForeignKey('professors.id'), nullable=True, unique=True)  # 1:1
    established_year = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)
    contact_email = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)

    head = relationship('Professor', uselist=False, foreign_keys=[head_id], post_update=True)
    professors = relationship('Professor', back_populates='department', foreign_keys='Professor.department_id')
    courses = relationship('Course', back_populates='department')