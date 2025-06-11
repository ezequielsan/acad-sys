from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.course import Course
from app.repositories.course_repository import CourseRepository
from app.services.course_service import CourseService
from typing import List
from app.api.schemas.course_schema import CourseRead, CourseCreate
from http import HTTPStatus
from datetime import date

router = APIRouter(prefix="/courses", tags=["Courses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/count", response_model=dict)
def count_courses(db: Session = Depends(get_db)):
    quantidade = db.query(Course).count()
    return {"quantidade": quantidade}

@router.get("/paged", response_model=List[CourseRead])
def paged_courses(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Limite de itens por página"),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    courses = db.query(Course).offset(offset).limit(limit).all()
    return [CourseService(CourseRepository(db))._to_dict(c) for c in courses]

@router.get("/filter", response_model=List[CourseRead])
def filter_courses(
    code: str = Query(None, description="Filtrar por código"),
    title: str = Query(None, description="Filtrar por título"),
    department_id: int = Query(None, description="Filtrar por departamento"),
    year: int = Query(None, description="Filtrar por ano"),
    db: Session = Depends(get_db)
):
    query = db.query(Course)
    if code:
        query = query.filter(Course.code.ilike(f"%{code}%"))
    if title:
        query = query.filter(Course.title.ilike(f"%{title}%"))
    if department_id:
        query = query.filter(Course.department_id == department_id)
    if year:
        query = query.filter(Course.year == year)
    courses = query.all()
    return [CourseService(CourseRepository(db))._to_dict(c) for c in courses]

@router.get("/search", response_model=List[CourseRead])
def search_courses(q: str = Query(..., description="Busca textual parcial no título ou descrição do curso"), db: Session = Depends(get_db)):
    query = db.query(Course).filter(
        (Course.title.ilike(f"%{q}%")) | (Course.description.ilike(f"%{q}%"))
    )
    courses = query.all()
    return [CourseService(CourseRepository(db))._to_dict(c) for c in courses]

@router.get("/by-department/{department_id}", response_model=List[CourseRead])
def courses_by_department(department_id: int, db: Session = Depends(get_db)):
    courses = db.query(Course).filter(Course.department_id == department_id).all()
    return [CourseService(CourseRepository(db))._to_dict(c) for c in courses]

@router.get("/ordered", response_model=List[CourseRead])
def ordered_courses(
    order_by: str = Query("title", description="Campo para ordenar (title, year, credits)"),
    desc: bool = Query(False, description="Ordem decrescente?"),
    db: Session = Depends(get_db)
):
    field = getattr(Course, order_by, Course.title)
    if desc:
        field = field.desc()
    courses = db.query(Course).order_by(field).all()
    return [CourseService(CourseRepository(db))._to_dict(c) for c in courses]

@router.get("/count-by-department/{department_id}", response_model=dict)
def count_courses_by_department(department_id: int, db: Session = Depends(get_db)):
    count = db.query(Course).filter(Course.department_id == department_id).count()
    return {"department_id": department_id, "quantidade": count}

@router.get("/with-department", response_model=List[dict])
def courses_with_department(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    result = []
    for course in courses:
        course_dict = CourseService(CourseRepository(db))._to_dict(course)
        dep = getattr(course, "department", None)
        course_dict["department"] = {"id": dep.id, "name": dep.name} if dep else None
        result.append(course_dict)
    return result

@router.get("/", response_model=List[CourseRead])
def list_courses(db: Session = Depends(get_db)):
    return CourseService(CourseRepository(db)).list_all()

@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    try:
        return CourseService(CourseRepository(db)).create(course.dict())
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Erro ao criar curso: {str(e)}. Verifique se os dados enviados são válidos."
        )

@router.post("/batch", response_model=List[CourseRead], status_code=status.HTTP_201_CREATED)
def create_courses_batch(courses: List[CourseCreate] = Body(...), db: Session = Depends(get_db)):
    try:
        return CourseService(CourseRepository(db)).create_many([c.dict() for c in courses])
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Erro ao criar cursos em lote: {str(e)}. Verifique se os dados enviados são válidos."
        )

@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    try:
        return CourseService(CourseRepository(db)).get_by_id(course_id)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Curso com id {course_id} não encontrado."
        )

@router.put("/{course_id}", response_model=CourseRead)
def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    try:
        return CourseService(CourseRepository(db)).update(course_id, course.dict())
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Não foi possível atualizar: curso com id {course_id} não encontrado."
        )

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        CourseService(CourseRepository(db)).delete(course_id)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Não foi possível remover: curso com id {course_id} não encontrado."
        )
    return None
