from app.repositories.professor_repository import ProfessorRepository
from app.db.models.professor import Professor
from app.utils.logger import logger
from typing import List, Optional

class ProfessorService:
    def __init__(self, repository: ProfessorRepository):
        self.repository = repository

    def list_all(self) -> List[dict]:
        logger.info("Listando todos os professores")
        return [self._to_dict(prof) for prof in self.repository.list_all()]

    def get_by_id(self, professor_id: int) -> dict:
        logger.info(f"Buscando professor por id: {professor_id}")
        prof = self.repository.get_by_id(professor_id)
        if not prof:
            logger.warning(f"Professor não encontrado: {professor_id}")
            raise Exception("Professor not found")
        return self._to_dict(prof)

    def create(self, professor_data: dict) -> dict:
        try:
            prof = self.repository.create(professor_data)
            logger.info(f"Professor criado: {prof.id} - {prof.first_name} {prof.last_name}")
            return self._to_dict(prof)
        except Exception as e:
            logger.error(f"Erro ao criar professor: {e}")
            raise

    def create_many(self, professors_data: List[dict]) -> List[dict]:
        created = []
        for data in professors_data:
            try:
                prof = self.repository.create(data)
                logger.info(f"Professor criado (lote): {prof.id} - {prof.first_name} {prof.last_name}")
                created.append(self._to_dict(prof))
            except Exception as e:
                logger.error(f"Erro ao criar professor em lote: {e}")
        logger.info(f"Lote de professores criado. Total: {len(created)}")
        return created

    def update(self, professor_id: int, professor_data: dict) -> dict:
        try:
            prof = self.repository.update(professor_id, professor_data)
            if not prof:
                logger.warning(f"Tentativa de atualizar professor inexistente: {professor_id}")
                raise Exception("Professor not found")
            logger.info(f"Professor atualizado: {prof.id} - {prof.first_name} {prof.last_name}")
            return self._to_dict(prof)
        except Exception as e:
            logger.error(f"Erro ao atualizar professor {professor_id}: {e}")
            raise

    def delete(self, professor_id: int) -> None:
        try:
            if not self.repository.delete(professor_id):
                logger.warning(f"Tentativa de deletar professor inexistente: {professor_id}")
                raise Exception("Professor not found")
            logger.info(f"Professor deletado: {professor_id}")
        except Exception as e:
            logger.error(f"Erro ao deletar professor {professor_id}: {e}")
            raise

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
