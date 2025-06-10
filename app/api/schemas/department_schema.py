from pydantic import BaseModel
from typing import Optional

class DepartmentBase(BaseModel):
    name: str
    head_id: Optional[int] = None
    established_year: Optional[int] = None
    description: Optional[str] = None
    contact_email: Optional[str] = None
    phone_number: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentRead(DepartmentBase):
    id: int
    class Config:
        orm_mode = True
