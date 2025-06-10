from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProfessorBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    hire_date: date
    department_id: Optional[int] = None
    title: Optional[str] = None

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorRead(ProfessorBase):
    id: int

    class Config:
        orm_mode = True
