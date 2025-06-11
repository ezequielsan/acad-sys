from sqlalchemy import Column, Integer, Float, Date, ForeignKey  # Importa os tipos de coluna e chaves estrangeiras do SQLAlchemy
from sqlalchemy.orm import relationship  # Importa a função para criar relacionamentos entre tabelas
from .base import Base  # Importa a classe base para os models ORM

class Enrollment(Base):  # Define a classe de matrícula herdando de Base
    __tablename__ = 'enrollments'  # Nome da tabela no banco de dados
    id = Column(Integer, primary_key=True, index=True)  # Chave primária da matrícula
    student_id = Column(Integer, ForeignKey('students.id'))  # Chave estrangeira para o aluno
    course_id = Column(Integer, ForeignKey('courses.id'))  # Chave estrangeira para o curso
    enrollment_date = Column(Date, nullable=False)  # Data da matrícula (obrigatória)
    grade = Column(Float, nullable=True)  # Nota final (opcional)
    completion_date = Column(Date, nullable=True)  # Data de conclusão (opcional)

    student = relationship('Student', back_populates='enrollments')  # Relacionamento com o aluno
    course = relationship('Course', back_populates='enrollments')  # Relacionamento com o curso
