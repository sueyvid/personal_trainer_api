# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

from app.core.database import engine, Base, init_db
from app.routers import auth, trainer, student, users, workouts

import asyncio

# Função para esperar o banco de dados
async def wait_for_db(max_retries: int = 10, delay: float = 2.0):
    """
    Tenta se conectar ao banco de dados com múltiplas tentativas.
    """
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("✅ Conexão com o banco de dados estabelecida.")
            return
        except OperationalError as e:
            print(f"⏳ Tentativa {attempt} falhou: {e}")
            await asyncio.sleep(delay)
    raise RuntimeError("❌ Não foi possível conectar ao banco de dados após várias tentativas.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Função que executa na inicialização e encerramento da API.
    """
    print("🚀 Serviço iniciando... aguardando banco de dados.")
    await wait_for_db()
    init_db()
    Base.metadata.create_all(bind=engine)
    yield
    print("🛑 Serviço encerrando.")

app = FastAPI(title="API Personal Trainer", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(trainer.router)
app.include_router(student.router)
