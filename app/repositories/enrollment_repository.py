from app.db.models.enrollment import Enrollment
from sqlalchemy.orm import Session
from typing import List, Optional

class EnrollmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> List[Enrollment]:
        return self.db.query(Enrollment).all()

    def get_by_id(self, enrollment_id: int) -> Optional[Enrollment]:
        return self.db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()

    def create(self, enrollment_data: dict) -> Enrollment:
        enrollment = Enrollment(**enrollment_data)
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment

    def update(self, enrollment_id: int, enrollment_data: dict) -> Optional[Enrollment]:
        enrollment = self.get_by_id(enrollment_id)
        if not enrollment:
            return None
        for key, value in enrollment_data.items():
            setattr(enrollment, key, value)
        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment

    def delete(self, enrollment_id: int) -> bool:
        enrollment = self.get_by_id(enrollment_id)
        if not enrollment:
            return False
        self.db.delete(enrollment)
        self.db.commit()
        return True
