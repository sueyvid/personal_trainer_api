import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Importações centralizadas e limpas
from app.core.dependencies import get_db
from app.core.security import create_access_token
from app.models.user import User
# ✅ Importa o novo UserLogin junto com os outros schemas
from app.schemas.user import UserCreate, UserOut, Token, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
# ✅ ATUALIZADO: Usa o schema UserLogin em vez de UserCreate
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    token = create_access_token({"sub": db_user.username, "role": db_user.role, "id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UserOut)
# A rota de registro continua usando UserCreate, o que está correto
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    db_user = User(
        username=user.username,
        hashed_password=hashed_pw.decode('utf-8'),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user