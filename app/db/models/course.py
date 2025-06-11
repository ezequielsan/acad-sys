from sqlalchemy import Column, Integer, String, ForeignKey  # Importa tipos de coluna e chaves estrangeiras
from sqlalchemy.orm import relationship  # Importa função para criar relacionamentos
from .base import Base  # Importa a classe base para os models ORM
from .professor import professor_course  # Importa a tabela associativa professor_curso

class Course(Base):  # Define a classe de curso herdando de Base
    __tablename__ = 'courses'  # Nome da tabela no banco de dados
    id = Column(Integer, primary_key=True, index=True)  # Chave primária do curso
    code = Column(String(20), nullable=False, unique=True)  # Código do curso (obrigatório e único)
    title = Column(String(100), nullable=False)  # Título do curso (obrigatório)
    credits = Column(Integer, nullable=False)  # Número de créditos (obrigatório)
    department_id = Column(Integer, ForeignKey('departments.id'))  # FK para departamento
    semester = Column(String(10), nullable=False)  # Semestre oferecido (obrigatório)
    year = Column(Integer, nullable=False)  # Ano oferecido (obrigatório)
    description = Column(String(255), nullable=True)  # Descrição do curso (opcional)
    prerequisites = Column(Integer, ForeignKey('courses.id'), nullable=True)  # FK para pré-requisito (opcional)
    max_enrollment = Column(Integer, nullable=False)  # Número máximo de estudantes (obrigatório)
    syllabus_url = Column(String(255), nullable=True)  # URL do plano de ensino (opcional)

    department = relationship('Department', back_populates='courses')  # Relacionamento com departamento
    professors = relationship('Professor', secondary=professor_course, back_populates='courses_taught')  # Relacionamento N:N com professores
    enrollments = relationship('Enrollment', back_populates='course')  # Relacionamento 1:N com matrículas
    prerequisite = relationship('Course', remote_side=[id], uselist=False)  # Relacionamento com o próprio curso (pré-requisito)