from app.repositories.enrollment_repository import EnrollmentRepository
from app.db.models.enrollment import Enrollment
from app.utils.logger import logger
from typing import List

class EnrollmentService:
    def __init__(self, repository: EnrollmentRepository):
        self.repository = repository

    def list_all(self) -> List[dict]:
        logger.info("Listando todas as matrículas")
        return [self._to_dict(enr) for enr in self.repository.list_all()]

    def get_by_id(self, enrollment_id: int) -> dict:
        logger.info(f"Buscando matrícula por id: {enrollment_id}")
        enr = self.repository.get_by_id(enrollment_id)
        if not enr:
            logger.warning(f"Matrícula não encontrada: {enrollment_id}")
            raise Exception("Enrollment not found")
        return self._to_dict(enr)

    def create(self, enrollment_data: dict) -> dict:
        try:
            enr = self.repository.create(enrollment_data)
            logger.info(f"Matrícula criada: {enr.id} - estudante {enr.student_id} no curso {enr.course_id}")
            return self._to_dict(enr)
        except Exception as e:
            logger.error(f"Erro ao criar matrícula: {e}")
            raise

    def create_many(self, enrollments_data: List[dict]) -> List[dict]:
        created = []
        for data in enrollments_data:
            try:
                enr = self.repository.create(data)
                logger.info(f"Matrícula criada (lote): {enr.id} - estudante {enr.student_id} no curso {enr.course_id}")
                created.append(self._to_dict(enr))
            except Exception as e:
                logger.error(f"Erro ao criar matrícula em lote: {e}")
        logger.info(f"Lote de matrículas criado. Total: {len(created)}")
        return created

    def update(self, enrollment_id: int, enrollment_data: dict) -> dict:
        try:
            enr = self.repository.update(enrollment_id, enrollment_data)
            if not enr:
                logger.warning(f"Tentativa de atualizar matrícula inexistente: {enrollment_id}")
                raise Exception("Enrollment not found")
            logger.info(f"Matrícula atualizada: {enr.id}")
            return self._to_dict(enr)
        except Exception as e:
            logger.error(f"Erro ao atualizar matrícula {enrollment_id}: {e}")
            raise

    def delete(self, enrollment_id: int) -> None:
        try:
            if not self.repository.delete(enrollment_id):
                logger.warning(f"Tentativa de deletar matrícula inexistente: {enrollment_id}")
                raise Exception("Enrollment not found")
            logger.info(f"Matrícula deletada: {enrollment_id}")
        except Exception as e:
            logger.error(f"Erro ao deletar matrícula {enrollment_id}: {e}")
            raise

    def _to_dict(self, enr: Enrollment) -> dict:
        return {
            "id": enr.id,
            "student_id": enr.student_id,
            "course_id": enr.course_id,
            "enrollment_date": str(enr.enrollment_date),
            "grade": enr.grade,
            "completion_date": str(enr.completion_date) if enr.completion_date is not None else None,
        }
