from app.db.models.course import Course
from sqlalchemy.orm import Session
from typing import List, Optional

class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> List[Course]:
        return self.db.query(Course).all()

    def get_by_id(self, course_id: int) -> Optional[Course]:
        return self.db.query(Course).filter(Course.id == course_id).first()

    def create(self, course_data: dict) -> Course:
        course = Course(**course_data)
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def update(self, course_id: int, course_data: dict) -> Optional[Course]:
        course = self.get_by_id(course_id)
        if not course:
            return None
        for key, value in course_data.items():
            setattr(course, key, value)
        self.db.commit()
        self.db.refresh(course)
        return course

    def delete(self, course_id: int) -> bool:
        course = self.get_by_id(course_id)
        if not course:
            return False
        self.db.delete(course)
        self.db.commit()
        return True
