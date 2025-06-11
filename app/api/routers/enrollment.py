from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.enrollment import Enrollment
from app.repositories.enrollment_repository import EnrollmentRepository
from app.services.enrollment_service import EnrollmentService
from typing import List
from app.api.schemas.enrollment_schema import EnrollmentRead, EnrollmentCreate
from http import HTTPStatus
from datetime import date

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/count", response_model=dict)
def count_enrollments(db: Session = Depends(get_db)):
    quantidade = db.query(Enrollment).count()
    return {"quantidade": quantidade}

@router.get("/paged", response_model=List[EnrollmentRead])
def paged_enrollments(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Limite de itens por página"),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    enrollments = db.query(Enrollment).offset(offset).limit(limit).all()
    return [EnrollmentService(EnrollmentRepository(db))._to_dict(e) for e in enrollments]

@router.get("/filter", response_model=List[EnrollmentRead])
def filter_enrollments(
    student_id: int = Query(None, description="Filtrar por estudante"),
    course_id: int = Query(None, description="Filtrar por curso"),
    db: Session = Depends(get_db)
):
    query = db.query(Enrollment)
    if student_id:
        query = query.filter(Enrollment.student_id == student_id)
    if course_id:
        query = query.filter(Enrollment.course_id == course_id)
    enrollments = query.all()
    return [EnrollmentService(EnrollmentRepository(db))._to_dict(e) for e in enrollments]

@router.get("/search", response_model=List[EnrollmentRead])
def search_enrollments(
    q: str = Query(..., description="Busca textual parcial por id do estudante ou curso"),
    db: Session = Depends(get_db)
):
    query = db.query(Enrollment).filter(
        (Enrollment.student_id == q) | (Enrollment.course_id == q)
    )
    enrollments = query.all()
    return [EnrollmentService(EnrollmentRepository(db))._to_dict(e) for e in enrollments]

@router.get("/by-student/{student_id}", response_model=List[EnrollmentRead])
def enrollments_by_student(student_id: int, db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == student_id).all()
    return [EnrollmentService(EnrollmentRepository(db))._to_dict(e) for e in enrollments]

@router.get("/by-course/{course_id}", response_model=List[EnrollmentRead])
def enrollments_by_course(course_id: int, db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).filter(Enrollment.course_id == course_id).all()
    return [EnrollmentService(EnrollmentRepository(db))._to_dict(e) for e in enrollments]

@router.get("/ordered", response_model=List[EnrollmentRead])
def ordered_enrollments(
    order_by: str = Query("enrollment_date", description="Campo para ordenar (enrollment_date, grade)"),
    desc: bool = Query(False, description="Ordem decrescente?"),
    db: Session = Depends(get_db)
):
    field = getattr(Enrollment, order_by, Enrollment.enrollment_date)
    if desc:
        field = field.desc()
    enrollments = db.query(Enrollment).order_by(field).all()
    return [EnrollmentService(EnrollmentRepository(db))._to_dict(e) for e in enrollments]

@router.get("/count-by-course/{course_id}", response_model=dict)
def count_enrollments_by_course(course_id: int, db: Session = Depends(get_db)):
    count = db.query(Enrollment).filter(Enrollment.course_id == course_id).count()
    return {"course_id": course_id, "quantidade": count}

@router.get("/with-student-course", response_model=List[dict])
def enrollments_with_student_course(db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).all()
    result = []
    for enr in enrollments:
        enr_dict = EnrollmentService(EnrollmentRepository(db))._to_dict(enr)
        stu = getattr(enr, "student", None)
        course = getattr(enr, "course", None)
        enr_dict["student"] = {"id": stu.id, "first_name": stu.first_name, "last_name": stu.last_name} if stu else None
        enr_dict["course"] = {"id": course.id, "title": course.title} if course else None
        result.append(enr_dict)
    return result

@router.get("/", response_model=List[EnrollmentRead])
def list_enrollments(db: Session = Depends(get_db)):
    return EnrollmentService(EnrollmentRepository(db)).list_all()

@router.post("/", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    try:
        return EnrollmentService(EnrollmentRepository(db)).create(enrollment.dict())
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Erro ao criar matrícula: {str(e)}. Verifique se os dados enviados são válidos."
        )

@router.post("/batch", response_model=List[EnrollmentRead], status_code=status.HTTP_201_CREATED)
def create_enrollments_batch(enrollments: List[EnrollmentCreate] = Body(...), db: Session = Depends(get_db)):
    try:
        return EnrollmentService(EnrollmentRepository(db)).create_many([e.dict() for e in enrollments])
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Erro ao criar matrículas em lote: {str(e)}. Verifique se os dados enviados são válidos."
        )

@router.get("/{enrollment_id}", response_model=EnrollmentRead)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    try:
        return EnrollmentService(EnrollmentRepository(db)).get_by_id(enrollment_id)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Matrícula com id {enrollment_id} não encontrada."
        )

@router.put("/{enrollment_id}", response_model=EnrollmentRead)
def update_enrollment(enrollment_id: int, enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    try:
        return EnrollmentService(EnrollmentRepository(db)).update(enrollment_id, enrollment.dict())
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Não foi possível atualizar: matrícula com id {enrollment_id} não encontrada."
        )

@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    try:
        EnrollmentService(EnrollmentRepository(db)).delete(enrollment_id)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Não foi possível remover: matrícula com id {enrollment_id} não encontrada."
        )
    return None
