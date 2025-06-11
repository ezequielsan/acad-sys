import app.db.models  # Garante que todos os models são importados
from fastapi import FastAPI
from app.api.routers import professor, department, student
from app.api.routers import course, enrollment

app = FastAPI()

app.include_router(professor.router)
app.include_router(department.router)
app.include_router(student.router)
app.include_router(course.router)
app.include_router(enrollment.router)

# Outros endpoints podem ser adicionados aqui futuramente

