from app.db.models.department import Department
from sqlalchemy.orm import Session
from typing import List, Optional

class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> List[Department]:
        return self.db.query(Department).all()

    def get_by_id(self, department_id: int) -> Optional[Department]:
        return self.db.query(Department).filter(Department.id == department_id).first()

    def create(self, department_data: dict) -> Department:
        department = Department(**department_data)
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)
        return department

    def update(self, department_id: int, department_data: dict) -> Optional[Department]:
        department = self.get_by_id(department_id)
        if not department:
            return None
        for key, value in department_data.items():
            setattr(department, key, value)
        self.db.commit()
        self.db.refresh(department)
        return department

    def delete(self, department_id: int) -> bool:
        department = self.get_by_id(department_id)
        if not department:
            return False
        self.db.delete(department)
        self.db.commit()
        return True
