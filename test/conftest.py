# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base
# ✅ ATUALIZADO: Importa 'get_db' do local centralizado de dependências
from app.core.dependencies import get_db 

# --- Configuração do Banco de Dados de Teste ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Sobrescrevendo a Dependência get_db ---
def override_get_db():
    database = None
    try:
        database = TestingSessionLocal()
        yield database
    finally:
        if database:
            database.close()


# Aplica a substituição na aplicação FastAPI
# Agora ele substitui a dependência 'get_db' correta em toda a aplicação
app.dependency_overrides[get_db] = override_get_db


# --- Fixture do Pytest para o Cliente da API ---
@pytest.fixture(scope="function")
def client():
    # Cria as tabelas no DB em memória antes de cada teste
    Base.metadata.create_all(bind=engine)
    
    yield TestClient(app)

    # Apaga tudo para o próximo teste ser executado de forma limpa
    Base.metadata.drop_all(bind=engine)