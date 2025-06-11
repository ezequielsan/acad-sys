from sqlalchemy import Column, Integer, String, ForeignKey  # Importa tipos de coluna e chaves estrangeiras
from sqlalchemy.orm import relationship  # Importa função para criar relacionamentos
from .base import Base  # Importa a classe base para os models ORM

class Department(Base):  # Define a classe de departamento herdando de Base
    __tablename__ = 'departments'  # Nome da tabela no banco de dados
    id = Column(Integer, primary_key=True, index=True)  # Chave primária do departamento
    name = Column(String(100), nullable=False)  # Nome do departamento (obrigatório)
    head_id = Column(Integer, ForeignKey('professors.id'), nullable=True, unique=True)  # FK para o chefe do departamento (professor)
    established_year = Column(Integer, nullable=True)  # Ano de fundação (opcional)
    description = Column(String(255), nullable=True)  # Descrição do departamento (opcional)
    contact_email = Column(String(100), nullable=True)  # E-mail de contato (opcional)
    phone_number = Column(String(20), nullable=True)  # Telefone de contato (opcional)

    head = relationship('Professor', uselist=False, foreign_keys=[head_id], post_update=True)  # Relacionamento 1:1 com o chefe
    professors = relationship('Professor', back_populates='department', foreign_keys='Professor.department_id')  # Relacionamento 1:N com professores
    courses = relationship('Course', back_populates='department')  # Relacionamento 1:N com cursos