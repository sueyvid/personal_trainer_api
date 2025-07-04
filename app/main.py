# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine, Base, init_db
from app.routers import auth, trainer, student, users, workouts


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Função que executa na inicialização e encerramento da API.
    """
    print("Serviço iniciando... conectando ao banco de dados.")
    # A inicialização acontece aqui, apenas quando a aplicação "sobe"
    init_db()
    Base.metadata.create_all(bind=engine)
    yield
    print("Serviço encerrando.")


# 3. A instância do FastAPI usa o lifespan
app = FastAPI(title="API Personal Trainer", lifespan=lifespan)

# 4. Inclusão das rotas
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(trainer.router)
app.include_router(student.router)
