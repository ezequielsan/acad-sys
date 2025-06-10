from app.db.models.student import Student
from sqlalchemy.orm import Session
from typing import List, Optional

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> List[Student]:
        return self.db.query(Student).all()

    def get_by_id(self, student_id: int) -> Optional[Student]:
        return self.db.query(Student).filter(Student.id == student_id).first()

    def create(self, student_data: dict) -> Student:
        student = Student(**student_data)
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def update(self, student_id: int, student_data: dict) -> Optional[Student]:
        student = self.get_by_id(student_id)
        if not student:
            return None
        for key, value in student_data.items():
            setattr(student, key, value)
        self.db.commit()
        self.db.refresh(student)
        return student

    def delete(self, student_id: int) -> bool:
        student = self.get_by_id(student_id)
        if not student:
            return False
        self.db.delete(student)
        self.db.commit()
        return True
