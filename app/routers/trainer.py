from fastapi import APIRouter, Depends
from app.core.dependencies import require_role

router = APIRouter(prefix="/trainer", tags=["trainer"])


@router.get("/dashboard", summary="Área restrita do treinador")
def trainer_dashboard(user=Depends(require_role("trainer"))):
    return {"msg": f"Bem-vindo treinador {user['username']}"}
