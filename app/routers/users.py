from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate, UserDelete

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.put("/me", response_model=UserOut)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_db = db.query(User).filter(User.username == current_user["username"]).first()
    if data.username:
        user_db.username = data.username
    if data.password:
        user_db.hashed_password = data.password  # ideal: aplicar hash
    db.commit()
    db.refresh(user_db)
    return user_db

@router.delete("/me")
def delete_me(
    data: UserDelete,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_db = db.query(User).filter(User.username == current_user["username"]).first()
    # aqui você deveria verificar o hash da senha
    if data.password != user_db.hashed_password:
        raise HTTPException(status_code=403, detail="Senha inválida")
    db.delete(user_db)
    db.commit()
    return {"message": "Conta excluída com sucesso"}
