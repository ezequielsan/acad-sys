from sqlalchemy import Column, Integer, String, Date  # Importa tipos de coluna do SQLAlchemy
from sqlalchemy.orm import relationship  # Importa função para criar relacionamentos
from .base import Base  # Importa a classe base para os models ORM

class Student(Base):  # Define a classe de estudante herdando de Base
    __tablename__ = 'students'  # Nome da tabela no banco de dados
    id = Column(Integer, primary_key=True, index=True)  # Chave primária do estudante
    first_name = Column(String(50), nullable=False)  # Primeiro nome (obrigatório)
    last_name = Column(String(50), nullable=False)  # Sobrenome (obrigatório)
    email = Column(String(100), nullable=False, unique=True)  # E-mail (obrigatório e único)
    birth_date = Column(Date, nullable=False)  # Data de nascimento (obrigatória)
    enrollment_date = Column(Date, nullable=False)  # Data de matrícula (obrigatória)
    major = Column(String(100), nullable=True)  # Curso/área de atuação (opcional)
    enrollment_number = Column(Integer, nullable=False, unique=True)  # Número de matrícula (obrigatório e único)

    enrollments = relationship('Enrollment', back_populates='student')  # Relacionamento com as matrículas