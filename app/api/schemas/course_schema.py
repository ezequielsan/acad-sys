from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    code: str
    title: str
    credits: int
    department_id: int
    semester: str
    year: int
    description: Optional[str] = None
    prerequisites: Optional[int] = None
    max_enrollment: int

class CourseCreate(CourseBase):
    pass

class CourseRead(CourseBase):
    id: int
    class Config:
        orm_mode = True
