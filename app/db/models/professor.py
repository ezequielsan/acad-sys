from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table  # Importa tipos de coluna e chaves estrangeiras
from sqlalchemy.orm import relationship  # Importa função para criar relacionamentos
from .base import Base  # Importa a classe base para os models ORM

# Tabela associativa para N:N entre Professor e Course
professor_course = Table(
    'professor_course', Base.metadata,  # Nome da tabela e metadata
    Column('professor_id', Integer, ForeignKey('professors.id'), primary_key=True),  # FK para professor
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)  # FK para curso
)

class Professor(Base):  # Define a classe de professor herdando de Base
    __tablename__ = 'professors'  # Nome da tabela no banco de dados
    id = Column(Integer, primary_key=True, index=True)  # Chave primária do professor
    first_name = Column(String(50), nullable=False)  # Primeiro nome (obrigatório)
    last_name = Column(String(50), nullable=False)  # Sobrenome (obrigatório)
    email = Column(String(100), nullable=False, unique=True)  # E-mail (obrigatório e único)
    hire_date = Column(Date, nullable=False)  # Data de contratação (obrigatória)
    department_id = Column(Integer, ForeignKey('departments.id'))  # FK para departamento
    title = Column(String(50), nullable=True)  # Título do professor (opcional)

    department = relationship('Department', back_populates='professors', foreign_keys=[department_id])  # Relacionamento com departamento
    courses_taught = relationship('Course', secondary=professor_course, back_populates='professors')  # Relacionamento N:N com cursos

