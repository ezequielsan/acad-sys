from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.repositories.student_repository import StudentRepository
from app.services.student_service import StudentService
from app.api.schemas.student_schema import StudentRead, StudentCreate
from typing import List

router = APIRouter(prefix="/students", tags=["Students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[StudentRead])
def list_students(db: Session = Depends(get_db)):
    return StudentService(StudentRepository(db)).list_all()

@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return StudentService(StudentRepository(db)).create(student.dict())

@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return StudentService(StudentRepository(db)).get_by_id(student_id)

@router.put("/{student_id}", response_model=StudentRead)
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    return StudentService(StudentRepository(db)).update(student_id, student.dict())

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    StudentService(StudentRepository(db)).delete(student_id)
    return None
