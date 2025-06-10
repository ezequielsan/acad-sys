import app.db.models  # Garante que todos os models são importados
from fastapi import FastAPI
from app.api.routers import professor, department, student

app = FastAPI()

app.include_router(professor.router)
app.include_router(department.router)
app.include_router(student.router)

# Outros endpoints podem ser adicionados aqui futuramente

