from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.professor import Professor
from app.repositories.professor_repository import ProfessorRepository
from app.services.professor_service import ProfessorService
from typing import List
from app.api.schemas.professor_schema import ProfessorRead, ProfessorCreate
from http import HTTPStatus
from datetime import date

router = APIRouter(prefix="/professors", tags=["Professors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ProfessorRead])
def list_professors(db: Session = Depends(get_db)):
    return ProfessorService(ProfessorRepository(db)).list_all()

@router.post("/", response_model=ProfessorRead, status_code=status.HTTP_201_CREATED)
def create_professor(professor: ProfessorCreate, db: Session = Depends(get_db)):
    try:
        return ProfessorService(ProfessorRepository(db)).create(professor.dict())
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Erro ao criar professor: {str(e)}. Verifique se os dados enviados são válidos e se o e-mail ou número de matrícula não estão duplicados."
        )

@router.post("/batch", response_model=List[ProfessorRead], status_code=status.HTTP_201_CREATED)
def create_professors_batch(professors: List[ProfessorCreate] = Body(...), db: Session = Depends(get_db)):
    try:
        return ProfessorService(ProfessorRepository(db)).create_many([p.dict() for p in professors])
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Erro ao criar professores em lote: {str(e)}. Verifique se os dados enviados são válidos."
        )

@router.get("/count", response_model=dict)
def count_professors(db: Session = Depends(get_db)):
    quantidade = db.query(Professor).count()
    return {"quantidade": quantidade}

@router.get("/paged", response_model=List[ProfessorRead])
def paged_professors(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Limite de itens por página"),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    profs = db.query(Professor).offset(offset).limit(limit).all()
    return [ProfessorService(ProfessorRepository(db))._to_dict(p) for p in profs]

@router.get("/filter", response_model=List[ProfessorRead])
def filter_professors(
    first_name: str = Query(None, description="Filtrar por nome"),
    last_name: str = Query(None, description="Filtrar por sobrenome"),
    email: str = Query(None, description="Filtrar por e-mail"),
    title: str = Query(None, description="Filtrar por título"),
    db: Session = Depends(get_db)
):
    query = db.query(Professor)
    if first_name:
        query = query.filter(Professor.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Professor.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Professor.email.ilike(f"%{email}%"))
    if title:
        query = query.filter(Professor.title.ilike(f"%{title}%"))
    profs = query.all()
    return [ProfessorService(ProfessorRepository(db))._to_dict(p) for p in profs]

@router.get("/search", response_model=List[ProfessorRead])
def search_professors(
    q: str = Query(..., description="Busca textual parcial no nome, sobrenome ou título"),
    db: Session = Depends(get_db)
):
    query = db.query(Professor).filter(
        (Professor.first_name.ilike(f"%{q}%")) |
        (Professor.last_name.ilike(f"%{q}%")) |
        (Professor.title.ilike(f"%{q}%"))
    )
    profs = query.all()
    return [ProfessorService(ProfessorRepository(db))._to_dict(p) for p in profs]

@router.get("/by-department/{department_id}", response_model=List[ProfessorRead])
def professors_by_department(department_id: int, db: Session = Depends(get_db)):
    profs = db.query(Professor).filter(Professor.department_id == department_id).all()
    return [ProfessorService(ProfessorRepository(db))._to_dict(p) for p in profs]

@router.get("/ordered", response_model=List[ProfessorRead])
def ordered_professors(
    order_by: str = Query("last_name", description="Campo para ordenar (first_name, last_name, hire_date)"),
    desc: bool = Query(False, description="Ordem decrescente?"),
    db: Session = Depends(get_db)
):
    field = getattr(Professor, order_by, Professor.last_name)
    if desc:
        field = field.desc()
    profs = db.query(Professor).order_by(field).all()
    return [ProfessorService(ProfessorRepository(db))._to_dict(p) for p in profs]

@router.get("/count-by-department/{department_id}", response_model=dict)
def count_professors_by_department(department_id: int, db: Session = Depends(get_db)):
    count = db.query(Professor).filter(Professor.department_id == department_id).count()
    return {"department_id": department_id, "quantidade": count}

@router.get("/with-department", response_model=List[dict])
def professors_with_department(db: Session = Depends(get_db)):
    profs = db.query(Professor).all()
    result = []
    for prof in profs:
        prof_dict = ProfessorService(ProfessorRepository(db))._to_dict(prof)
        dep = getattr(prof, "department", None)
        prof_dict["department"] = {"id": dep.id, "name": dep.name} if dep else None
        result.append(prof_dict)
    return result

@router.get("/{professor_id}", response_model=ProfessorRead)
def get_professor(professor_id: int, db: Session = Depends(get_db)):
    try:
        return ProfessorService(ProfessorRepository(db)).get_by_id(professor_id)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Professor com id {professor_id} não encontrado."
        )

@router.put("/{professor_id}", response_model=ProfessorRead)
def update_professor(professor_id: int, professor: ProfessorCreate, db: Session = Depends(get_db)):
    try:
        return ProfessorService(ProfessorRepository(db)).update(professor_id, professor.dict())
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Não foi possível atualizar: professor com id {professor_id} não encontrado."
        )

@router.delete("/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    try:
        ProfessorService(ProfessorRepository(db)).delete(professor_id)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Não foi possível remover: professor com id {professor_id} não encontrado."
        )
    return None
