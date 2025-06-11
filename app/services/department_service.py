from app.repositories.department_repository import DepartmentRepository
from app.db.models.department import Department
from app.utils.logger import logger
from typing import List

class DepartmentService:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    def list_all(self) -> List[dict]:
        logger.info("Listando todos os departamentos")
        return [self._to_dict(dep) for dep in self.repository.list_all()]

    def get_by_id(self, department_id: int) -> dict:
        logger.info(f"Buscando departamento por id: {department_id}")
        dep = self.repository.get_by_id(department_id)
        if not dep:
            logger.warning(f"Departamento não encontrado: {department_id}")
            raise Exception("Department not found")
        return self._to_dict(dep)

    def create(self, department_data: dict) -> dict:
        try:
            dep = self.repository.create(department_data)
            logger.info(f"Departamento criado: {dep.id} - {dep.name}")
            return self._to_dict(dep)
        except Exception as e:
            logger.error(f"Erro ao criar departamento: {e}")
            raise

    def create_many(self, departments_data: List[dict]) -> List[dict]:
        created = []
        for data in departments_data:
            try:
                dep = self.repository.create(data)
                logger.info(f"Departamento criado (lote): {dep.id} - {dep.name}")
                created.append(self._to_dict(dep))
            except Exception as e:
                logger.error(f"Erro ao criar departamento em lote: {e}")
        logger.info(f"Lote de departamentos criado. Total: {len(created)}")
        return created

    def update(self, department_id: int, department_data: dict) -> dict:
        try:
            dep = self.repository.update(department_id, department_data)
            if not dep:
                logger.warning(f"Tentativa de atualizar departamento inexistente: {department_id}")
                raise Exception("Department not found")
            logger.info(f"Departamento atualizado: {dep.id} - {dep.name}")
            return self._to_dict(dep)
        except Exception as e:
            logger.error(f"Erro ao atualizar departamento {department_id}: {e}")
            raise

    def delete(self, department_id: int) -> None:
        try:
            if not self.repository.delete(department_id):
                logger.warning(f"Tentativa de deletar departamento inexistente: {department_id}")
                raise Exception("Department not found")
            logger.info(f"Departamento deletado: {department_id}")
        except Exception as e:
            logger.error(f"Erro ao deletar departamento {department_id}: {e}")
            raise

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
