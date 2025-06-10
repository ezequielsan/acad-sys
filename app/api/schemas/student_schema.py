from pydantic import BaseModel
from typing import Optional
from datetime import date

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    birth_date: date
    enrollment_date: date
    major: Optional[str] = None
    enrollment_number: int

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: int
    class Config:
        orm_mode = True
