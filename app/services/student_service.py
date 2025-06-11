from app.repositories.student_repository import StudentRepository
from app.db.models.student import Student
from app.utils.logger import logger
from typing import List

class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def list_all(self) -> List[dict]:
        logger.info("Listando todos os estudantes")
        return [self._to_dict(stu) for stu in self.repository.list_all()]

    def get_by_id(self, student_id: int) -> dict:
        logger.info(f"Buscando estudante por id: {student_id}")
        stu = self.repository.get_by_id(student_id)
        if not stu:
            logger.warning(f"Estudante não encontrado: {student_id}")
            raise Exception("Student not found")
        return self._to_dict(stu)

    def create(self, student_data: dict) -> dict:
        try:
            stu = self.repository.create(student_data)
            logger.info(f"Estudante criado: {stu.id} - {stu.first_name} {stu.last_name}")
            return self._to_dict(stu)
        except Exception as e:
            logger.error(f"Erro ao criar estudante: {e}")
            raise

    def create_many(self, students_data: List[dict]) -> List[dict]:
        created = []
        for data in students_data:
            try:
                stu = self.repository.create(data)
                logger.info(f"Estudante criado (lote): {stu.id} - {stu.first_name} {stu.last_name}")
                created.append(self._to_dict(stu))
            except Exception as e:
                logger.error(f"Erro ao criar estudante em lote: {e}")
                # Continua para o próximo registro
        logger.info(f"Lote de estudantes criado. Total: {len(created)}")
        return created

    def update(self, student_id: int, student_data: dict) -> dict:
        try:
            stu = self.repository.update(student_id, student_data)
            if not stu:
                logger.warning(f"Tentativa de atualizar estudante inexistente: {student_id}")
                raise Exception("Student not found")
            logger.info(f"Estudante atualizado: {stu.id} - {stu.first_name} {stu.last_name}")
            return self._to_dict(stu)
        except Exception as e:
            logger.error(f"Erro ao atualizar estudante {student_id}: {e}")
            raise

    def delete(self, student_id: int) -> None:
        try:
            if not self.repository.delete(student_id):
                logger.warning(f"Tentativa de deletar estudante inexistente: {student_id}")
                raise Exception("Student not found")
            logger.info(f"Estudante deletado: {student_id}")
        except Exception as e:
            logger.error(f"Erro ao deletar estudante {student_id}: {e}")
            raise

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
