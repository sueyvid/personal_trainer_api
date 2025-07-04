# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ✅ Importa o objeto settings centralizado
from app.core.config import settings

# ✅ Usa a DATABASE_URL do objeto settings
# Não precisamos mais de os.getenv() ou de checagens manuais aqui
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
