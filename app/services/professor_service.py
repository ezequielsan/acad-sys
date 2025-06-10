from app.repositories.professor_repository import ProfessorRepository
from app.db.models.professor import Professor
from typing import List, Optional

class ProfessorService:
    def __init__(self, repository: ProfessorRepository):
        self.repository = repository

    def list_all(self) -> List[dict]:
        return [self._to_dict(prof) for prof in self.repository.list_all()]

    def get_by_id(self, professor_id: int) -> dict:
        prof = self.repository.get_by_id(professor_id)
        if not prof:
            raise Exception("Professor not found")
        return self._to_dict(prof)

    def create(self, professor_data: dict) -> dict:
        prof = self.repository.create(professor_data)
        return self._to_dict(prof)

    def update(self, professor_id: int, professor_data: dict) -> dict:
        prof = self.repository.update(professor_id, professor_data)
        if not prof:
            raise Exception("Professor not found")
        return self._to_dict(prof)

    def delete(self, professor_id: int) -> None:
        if not self.repository.delete(professor_id):
            raise Exception("Professor not found")

    def _to_dict(self, prof: Professor) -> dict:
        return {
            "id": prof.id,
            "first_name": prof.first_name,
            "last_name": prof.last_name,
            "email": prof.email,
            "hire_date": str(prof.hire_date),
            "department_id": prof.department_id,
            "title": prof.title,
        }
