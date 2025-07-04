import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ✅ Lê a variável de ambiente injetada pelo Docker Compose
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Adiciona uma verificação para dar um erro claro se a variável não for encontrada
if DATABASE_URL is None:
    raise ValueError("A variável de ambiente DATABASE_URL não foi definida.")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função init_db (se você a usa)
def init_db():
    Base.metadata.create_all(bind=engine)