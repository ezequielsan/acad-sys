from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.student import Student
from app.repositories.student_repository import StudentRepository
from app.services.student_service import StudentService
from typing import List
from app.api.schemas.student_schema import StudentRead, StudentCreate
from http import HTTPStatus
from datetime import date

router = APIRouter(prefix="/students", tags=["Students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/count", response_model=dict)
def count_students(db: Session = Depends(get_db)):
    quantidade = db.query(Student).count()
    return {"quantidade": quantidade}

@router.get("/paged", response_model=List[StudentRead])
def paged_students(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Limite de itens por página"),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    students = db.query(Student).offset(offset).limit(limit).all()
    return [StudentService(StudentRepository(db))._to_dict(s) for s in students]

@router.get("/filter", response_model=List[StudentRead])
def filter_students(
    first_name: str = Query(None, description="Filtrar por nome"),
    last_name: str = Query(None, description="Filtrar por sobrenome"),
    email: str = Query(None, description="Filtrar por e-mail"),
    major: str = Query(None, description="Filtrar por curso/área"),
    db: Session = Depends(get_db)
):
    query = db.query(Student)
    if first_name:
        query = query.filter(Student.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Student.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Student.email.ilike(f"%{email}%"))
    if major:
        query = query.filter(Student.major.ilike(f"%{major}%"))
    students = query.all()
    return [StudentService(StudentRepository(db))._to_dict(s) for s in students]

@router.get("/search", response_model=List[StudentRead])
def search_students(
    q: str = Query(..., description="Busca textual parcial no nome, sobrenome, email ou major"),
    db: Session = Depends(get_db)
):
    query = db.query(Student).filter(
        (Student.first_name.ilike(f"%{q}%")) |
        (Student.last_name.ilike(f"%{q}%")) |
        (Student.email.ilike(f"%{q}%")) |
        (Student.major.ilike(f"%{q}%"))
    )
    students = query.all()
    return [StudentService(StudentRepository(db))._to_dict(s) for s in students]

@router.get("/by-major/{major}", response_model=List[StudentRead])
def students_by_major(major: str, db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.major.ilike(f"%{major}%")).all()
    return [StudentService(StudentRepository(db))._to_dict(s) for s in students]

@router.get("/ordered", response_model=List[StudentRead])
def ordered_students(
    order_by: str = Query("last_name", description="Campo para ordenar (first_name, last_name, enrollment_date)"),
    desc: bool = Query(False, description="Ordem decrescente?"),
    db: Session = Depends(get_db)
):
    field = getattr(Student, order_by, Student.last_name)
    if desc:
        field = field.desc()
    students = db.query(Student).order_by(field).all()
    return [StudentService(StudentRepository(db))._to_dict(s) for s in students]

@router.get("/count-by-major/{major}", response_model=dict)
def count_students_by_major(major: str, db: Session = Depends(get_db)):
    count = db.query(Student).filter(Student.major.ilike(f"%{major}%")).count()
    return {"major": major, "quantidade": count}

@router.get("/by-enrollment-year/{year}", response_model=List[StudentRead])
def students_by_enrollment_year(year: int, db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.enrollment_date.between(f"{year}-01-01", f"{year}-12-31")).all()
    return [StudentService(StudentRepository(db))._to_dict(s) for s in students]

@router.get("/with-department", response_model=List[dict])
def students_with_department(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    result = []
    for stu in students:
        stu_dict = StudentService(StudentRepository(db))._to_dict(stu)
        dep = getattr(stu, "department", None)
        stu_dict["department"] = {"id": dep.id, "name": dep.name} if dep else None
        result.append(stu_dict)
    return result

@router.get("/", response_model=List[StudentRead])
def list_students(db: Session = Depends(get_db)):
    return StudentService(StudentRepository(db)).list_all()

@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    try:
        return StudentService(StudentRepository(db)).create(student.dict())
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Erro ao criar estudante: {str(e)}. Verifique se os dados enviados são válidos e se o e-mail ou número de matrícula não estão duplicados."
        )

@router.post("/batch", response_model=List[StudentRead], status_code=status.HTTP_201_CREATED)
def create_students_batch(students: List[StudentCreate] = Body(...), db: Session = Depends(get_db)):
    try:
        return StudentService(StudentRepository(db)).create_many([s.dict() for s in students])
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Erro ao criar estudantes em lote: {str(e)}. Verifique se os dados enviados são válidos."
        )

@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    try:
        return StudentService(StudentRepository(db)).get_by_id(student_id)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Estudante com id {student_id} não encontrado."
        )

@router.put("/{student_id}", response_model=StudentRead)
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    try:
        return StudentService(StudentRepository(db)).update(student_id, student.dict())
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Não foi possível atualizar: estudante com id {student_id} não encontrado."
        )

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    try:
        StudentService(StudentRepository(db)).delete(student_id)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Não foi possível remover: estudante com id {student_id} não encontrado."
        )
    return None
