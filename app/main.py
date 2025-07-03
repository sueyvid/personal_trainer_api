from app.core.database import init_db
init_db()

from app.core.database import Base, engine
from app.models.user import User

Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from app.routers import auth, trainer, student

app = FastAPI(title="API Personal Trainer")

app.include_router(auth.router)
app.include_router(trainer.router)
app.include_router(student.router)
