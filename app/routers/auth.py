from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, Token
from app.core.security import create_access_token

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
import bcrypt

router = APIRouter(prefix="/auth", tags=["auth"])

# dependência para injetar sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    token = create_access_token({"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # verifica se já existe
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    # faz hash da senha
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
