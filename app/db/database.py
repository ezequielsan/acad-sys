import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

# Carrega variáveis do .env
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

# Configurar o logger 
logging.basicConfig() 
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Configuração do banco de dados 
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
