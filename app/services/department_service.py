from app.repositories.department_repository import DepartmentRepository
from app.db.models.department import Department
from typing import List

class DepartmentService:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    def list_all(self) -> List[dict]:
        return [self._to_dict(dep) for dep in self.repository.list_all()]

    def get_by_id(self, department_id: int) -> dict:
        dep = self.repository.get_by_id(department_id)
        if not dep:
            raise Exception("Department not found")
        return self._to_dict(dep)

    def create(self, department_data: dict) -> dict:
        dep = self.repository.create(department_data)
        return self._to_dict(dep)

    def update(self, department_id: int, department_data: dict) -> dict:
        dep = self.repository.update(department_id, department_data)
        if not dep:
            raise Exception("Department not found")
        return self._to_dict(dep)

    def delete(self, department_id: int) -> None:
        if not self.repository.delete(department_id):
            raise Exception("Department not found")

    def _to_dict(self, dep: Department) -> dict:
        return {
            "id": dep.id,
            "name": dep.name,
            "head_id": dep.head_id,
            "established_year": dep.established_year,
            "description": dep.description,
            "contact_email": dep.contact_email,
            "phone_number": dep.phone_number,
        }
