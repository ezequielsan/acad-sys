from app.db.models.professor import Professor
from sqlalchemy.orm import Session
from typing import List, Optional

class ProfessorRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> List[Professor]:
        return self.db.query(Professor).all()

    def get_by_id(self, professor_id: int) -> Optional[Professor]:
        return self.db.query(Professor).filter(Professor.id == professor_id).first()

    def create(self, professor_data: dict) -> Professor:
        professor = Professor(**professor_data)
        self.db.add(professor)
        self.db.commit()
        self.db.refresh(professor)
        return professor

    def update(self, professor_id: int, professor_data: dict) -> Optional[Professor]:
        professor = self.get_by_id(professor_id)
        if not professor:
            return None
        for key, value in professor_data.items():
            setattr(professor, key, value)
        self.db.commit()
        self.db.refresh(professor)
        return professor

    def delete(self, professor_id: int) -> bool:
        professor = self.get_by_id(professor_id)
        if not professor:
            return False
        self.db.delete(professor)
        self.db.commit()
        return True
