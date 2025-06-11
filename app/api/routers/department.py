from fastapi import APIRouter, Depends, status, HTTPException, Query, Body
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.repositories.department_repository import DepartmentRepository
from app.services.department_service import DepartmentService
from app.api.schemas.department_schema import DepartmentRead, DepartmentCreate
from app.db.models.department import Department
from typing import List
from http import HTTPStatus
from datetime import date

router = APIRouter(prefix="/departments", tags=["Departments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/count", response_model=dict)
def count_departments(db: Session = Depends(get_db)):
    quantidade = db.query(Department).count()
    return {"quantidade": quantidade}

@router.get("/paged", response_model=List[DepartmentRead])
def paged_departments(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Limite de itens por página"),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    deps = db.query(Department).offset(offset).limit(limit).all()
    return [DepartmentService(DepartmentRepository(db))._to_dict(d) for d in deps]

@router.get("/filter", response_model=List[DepartmentRead])
def filter_departments(
    name: str = Query(None, description="Filtrar por nome"),
    description: str = Query(None, description="Filtrar por descrição"),
    contact_email: str = Query(None, description="Filtrar por e-mail de contato"),
    db: Session = Depends(get_db)
):
    query = db.query(Department)
    if name:
        query = query.filter(Department.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(Department.description.ilike(f"%{description}%"))
    if contact_email:
        query = query.filter(Department.contact_email.ilike(f"%{contact_email}%"))
    deps = query.all()
    return [DepartmentService(DepartmentRepository(db))._to_dict(d) for d in deps]

@router.get("/search", response_model=List[DepartmentRead])
def search_departments(
    q: str = Query(..., description="Busca textual parcial no nome ou descrição do departamento"),
    db: Session = Depends(get_db)
):
    query = db.query(Department).filter(
        (Department.name.ilike(f"%{q}%")) | (Department.description.ilike(f"%{q}%"))
    )
    deps = query.all()
    return [DepartmentService(DepartmentRepository(db))._to_dict(d) for d in deps]

@router.get("/by-year", response_model=List[DepartmentRead])
def departments_by_year(
    year: int = Query(..., description="Ano de fundação do departamento"),
    db: Session = Depends(get_db)
):
    deps = db.query(Department).filter(Department.established_year == year).all()
    return [DepartmentService(DepartmentRepository(db))._to_dict(d) for d in deps]

@router.get("/count-by-year", response_model=dict)
def count_departments_by_year(
    year: int = Query(..., description="Ano de fundação do departamento"),
    db: Session = Depends(get_db)
):
    count = db.query(Department).filter(Department.established_year == year).count()
    return {"ano": year, "quantidade": count}

@router.get("/ordered", response_model=List[DepartmentRead])
def ordered_departments(
    order_by: str = Query("name", description="Campo para ordenar (name, established_year)"),
    desc: bool = Query(False, description="Ordem decrescente?"),
    db: Session = Depends(get_db)
):
    field = getattr(Department, order_by, Department.name)
    if desc:
        field = field.desc()
    deps = db.query(Department).order_by(field).all()
    return [DepartmentService(DepartmentRepository(db))._to_dict(d) for d in deps]

@router.get("/with-professors", response_model=List[dict])
def departments_with_professors(db: Session = Depends(get_db)):
    deps = db.query(Department).all()
    result = []
    for dep in deps:
        dep_dict = DepartmentService(DepartmentRepository(db))._to_dict(dep)
        dep_dict["professors"] = [
            {"id": p.id, "first_name": p.first_name, "last_name": p.last_name, "email": p.email}
            for p in getattr(dep, "professors", [])
        ]
        result.append(dep_dict)
    return result

@router.get("/", response_model=List[DepartmentRead])
def list_departments(db: Session = Depends(get_db)):
    return DepartmentService(DepartmentRepository(db)).list_all()

@router.post("/", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    try:
        return DepartmentService(DepartmentRepository(db)).create(department.dict())
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Erro ao criar departamento: {str(e)}. Verifique se os dados enviados são válidos."
        )

@router.post("/batch", response_model=List[DepartmentRead], status_code=status.HTTP_201_CREATED)
def create_departments_batch(departments: List[DepartmentCreate] = Body(...), db: Session = Depends(get_db)):
    try:
        return DepartmentService(DepartmentRepository(db)).create_many([d.dict() for d in departments])
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Erro ao criar departamentos em lote: {str(e)}. Verifique se os dados enviados são válidos."
        )

@router.get("/{department_id}", response_model=DepartmentRead)
def get_department(department_id: int, db: Session = Depends(get_db)):
    try:
        return DepartmentService(DepartmentRepository(db)).get_by_id(department_id)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Departamento com id {department_id} não encontrado."
        )

@router.put("/{department_id}", response_model=DepartmentRead)
def update_department(department_id: int, department: DepartmentCreate, db: Session = Depends(get_db)):
    try:
        return DepartmentService(DepartmentRepository(db)).update(department_id, department.dict())
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Não foi possível atualizar: departamento com id {department_id} não encontrado."
        )

@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    try:
        DepartmentService(DepartmentRepository(db)).delete(department_id)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Não foi possível remover: departamento com id {department_id} não encontrado."
        )
    return None
