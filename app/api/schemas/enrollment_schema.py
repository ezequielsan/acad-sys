from pydantic import BaseModel
from typing import Optional
from datetime import date

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date
    grade: Optional[float] = None
    completion_date: Optional[date] = None

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentRead(EnrollmentBase):
    id: int
    class Config:
        orm_mode = True
