from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

Base = declarative_base()
SessionLocal = None
engine = None

def init_db():
    global SessionLocal, engine
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/personal_trainer"
    )
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
