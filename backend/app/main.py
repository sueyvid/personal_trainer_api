# app/main.py

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← ADICIONADO AQUI
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.core.database import Base, engine, init_db
from app.routers import auth, student, trainer, users, workouts, progress
from app.routers.exercises import router as exercises_router


# Função para esperar o banco de dados
async def wait_for_db(max_retries: int = 10, delay: float = 2.0):
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
    print("🚀 Serviço iniciando... aguardando banco de dados.")
    await wait_for_db()
    init_db()
    Base.metadata.create_all(bind=engine)
    yield
    print("🛑 Serviço encerrando.")


app = FastAPI(title="API Personal Trainer", lifespan=lifespan)

# ✅ CONFIGURAÇÃO DE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ou ["*"] para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(trainer.router)
app.include_router(student.router)
app.include_router(progress.router)
app.include_router(exercises_router)
