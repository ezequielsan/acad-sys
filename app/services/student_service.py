from app.repositories.student_repository import StudentRepository
from app.db.models.student import Student
from typing import List

class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def list_all(self) -> List[dict]:
        return [self._to_dict(stu) for stu in self.repository.list_all()]

    def get_by_id(self, student_id: int) -> dict:
        stu = self.repository.get_by_id(student_id)
        if not stu:
            raise Exception("Student not found")
        return self._to_dict(stu)

    def create(self, student_data: dict) -> dict:
        stu = self.repository.create(student_data)
        return self._to_dict(stu)

    def update(self, student_id: int, student_data: dict) -> dict:
        stu = self.repository.update(student_id, student_data)
        if not stu:
            raise Exception("Student not found")
        return self._to_dict(stu)

    def delete(self, student_id: int) -> None:
        if not self.repository.delete(student_id):
            raise Exception("Student not found")

    def _to_dict(self, stu: Student) -> dict:
        return {
            "id": stu.id,
            "first_name": stu.first_name,
            "last_name": stu.last_name,
            "email": stu.email,
            "birth_date": str(stu.birth_date),
            "enrollment_date": str(stu.enrollment_date),
            "major": stu.major,
            "enrollment_number": stu.enrollment_number,
        }
