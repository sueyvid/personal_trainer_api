import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.user import User

from app.schemas.user import UserOut, UserUpdate, UserDelete

router = APIRouter(prefix="/users", tags=["users"])


# Esta rota não tem conflitos e já está correta.
@router.put("/me", response_model=UserOut)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_db = db.query(User).filter(User.username == current_user["username"]).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if data.password:
        hashed_pw = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt())
        user_db.hashed_password = hashed_pw.decode("utf-8")

    db.commit()
    db.refresh(user_db)
    return user_db


@router.delete("/me", status_code=204)
def delete_me(
    data: UserDelete,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_db = db.query(User).filter(User.username == current_user["username"]).first()

    if not user_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not bcrypt.checkpw(
        data.password.encode("utf-8"), user_db.hashed_password.encode("utf-8")
    ):
        raise HTTPException(
            status_code=403, detail="Senha inválida para exclusão da conta."
        )

    db.delete(user_db)
    db.commit()
    # Um status 204 (No Content) não deve retornar um corpo de mensagem.
    return
