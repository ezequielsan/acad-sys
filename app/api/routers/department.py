from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.repositories.department_repository import DepartmentRepository
from app.services.department_service import DepartmentService
from app.api.schemas.department_schema import DepartmentRead, DepartmentCreate
from typing import List

router = APIRouter(prefix="/departments", tags=["Departments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[DepartmentRead])
def list_departments(db: Session = Depends(get_db)):
    return DepartmentService(DepartmentRepository(db)).list_all()

@router.post("/", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    return DepartmentService(DepartmentRepository(db)).create(department.dict())

@router.get("/{department_id}", response_model=DepartmentRead)
def get_department(department_id: int, db: Session = Depends(get_db)):
    return DepartmentService(DepartmentRepository(db)).get_by_id(department_id)

@router.put("/{department_id}", response_model=DepartmentRead)
def update_department(department_id: int, department: DepartmentCreate, db: Session = Depends(get_db)):
    return DepartmentService(DepartmentRepository(db)).update(department_id, department.dict())

@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    DepartmentService(DepartmentRepository(db)).delete(department_id)
    return None
