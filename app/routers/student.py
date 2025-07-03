from fastapi import APIRouter, Depends
from app.core.dependencies import require_role

router = APIRouter(
    prefix="/student",
    tags=["student"]
)

@router.get("/dashboard", summary="Área restrita do aluno")
def student_dashboard(user=Depends(require_role("student"))):
    return {"msg": f"Bem-vindo aluno {user['username']}"}
