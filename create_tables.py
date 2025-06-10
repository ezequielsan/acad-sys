from app.db.database import engine
from app.db.models.base import Base
import app.db.models.department
import app.db.models.professor
import app.db.models.course
import app.db.models.student
import app.db.models.enrollment

print('Database URL:', engine.url)
Base.metadata.create_all(bind=engine)
print('Tabelas criadas!')
