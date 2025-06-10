from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.professor import Professor
from app.repositories.professor_repository import ProfessorRepository
from app.services.professor_service import ProfessorService
from typing import List
from app.api.schemas.professor_schema import ProfessorRead, ProfessorCreate

router = APIRouter(prefix="/professors", tags=["Professors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ProfessorRead])
def list_professors(db: Session = Depends(get_db)):
    return ProfessorService(ProfessorRepository(db)).list_all()

@router.post("/", response_model=ProfessorRead, status_code=status.HTTP_201_CREATED)
def create_professor(professor: ProfessorCreate, db: Session = Depends(get_db)):
    return ProfessorService(ProfessorRepository(db)).create(professor.dict())

@router.get("/{professor_id}", response_model=ProfessorRead)
def get_professor(professor_id: int, db: Session = Depends(get_db)):
    return ProfessorService(ProfessorRepository(db)).get_by_id(professor_id)

@router.put("/{professor_id}", response_model=ProfessorRead)
def update_professor(professor_id: int, professor: ProfessorCreate, db: Session = Depends(get_db)):
    return ProfessorService(ProfessorRepository(db)).update(professor_id, professor.dict())

@router.delete("/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    ProfessorService(ProfessorRepository(db)).delete(professor_id)
    return None
