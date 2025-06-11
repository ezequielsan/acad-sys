from app.repositories.course_repository import CourseRepository
from app.db.models.course import Course
from app.utils.logger import logger
from typing import List

class CourseService:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    def list_all(self) -> List[dict]:
        logger.info("Listando todos os cursos")
        return [self._to_dict(course) for course in self.repository.list_all()]

    def get_by_id(self, course_id: int) -> dict:
        logger.info(f"Buscando curso por id: {course_id}")
        course = self.repository.get_by_id(course_id)
        if not course:
            logger.warning(f"Curso não encontrado: {course_id}")
            raise Exception("Course not found")
        return self._to_dict(course)

    def create(self, course_data: dict) -> dict:
        try:
            course = self.repository.create(course_data)
            logger.info(f"Curso criado: {course.id} - {course.title}")
            return self._to_dict(course)
        except Exception as e:
            logger.error(f"Erro ao criar curso: {e}")
            raise

    def create_many(self, courses_data: List[dict]) -> List[dict]:
        created = []
        for data in courses_data:
            try:
                course = self.repository.create(data)
                logger.info(f"Curso criado (lote): {course.id} - {course.title}")
                created.append(self._to_dict(course))
            except Exception as e:
                logger.error(f"Erro ao criar curso em lote: {e}")
        logger.info(f"Lote de cursos criado. Total: {len(created)}")
        return created

    def update(self, course_id: int, course_data: dict) -> dict:
        try:
            course = self.repository.update(course_id, course_data)
            if not course:
                logger.warning(f"Tentativa de atualizar curso inexistente: {course_id}")
                raise Exception("Course not found")
            logger.info(f"Curso atualizado: {course.id} - {course.title}")
            return self._to_dict(course)
        except Exception as e:
            logger.error(f"Erro ao atualizar curso {course_id}: {e}")
            raise

    def delete(self, course_id: int) -> None:
        try:
            if not self.repository.delete(course_id):
                logger.warning(f"Tentativa de deletar curso inexistente: {course_id}")
                raise Exception("Course not found")
            logger.info(f"Curso deletado: {course_id}")
        except Exception as e:
            logger.error(f"Erro ao deletar curso {course_id}: {e}")
            raise

    def _to_dict(self, course: Course) -> dict:
        return {
            "id": course.id,
            "code": course.code,
            "title": course.title,
            "credits": course.credits,
            "department_id": course.department_id,
            "semester": course.semester,
            "year": course.year,
            "description": course.description,
            "prerequisites": course.prerequisites,
            "max_enrollment": course.max_enrollment,
        }
