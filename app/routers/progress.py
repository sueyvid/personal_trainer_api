# app/routers/progress.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_role
from app.models.progress import Progress
from app.schemas.progress import ProgressCreate, ProgressOut
from app.models.workout import Workout


router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("/", response_model=ProgressOut)
def mark_progress(
    data: ProgressCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("student")),
):
    # Verifica se o treino existe e pertence ao aluno
    workout = (
        db.query(Workout)
        .filter(Workout.id == data.workout_id, Workout.student_id == current_user["id"])
        .first()
    )

    if not workout:
        raise HTTPException(
            status_code=404, detail="Treino não encontrado ou não pertence a você."
        )

    # Impede duplicidade
    existing = (
        db.query(Progress)
        .filter_by(
            student_id=current_user["id"],
            workout_id=data.workout_id,
            date=data.date,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400, detail="Progresso já marcado para esse dia."
        )

    progress = Progress(**data.dict(), student_id=current_user["id"])
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


@router.get("/me", response_model=list[ProgressOut])
def list_my_progress(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("student")),
):
    return db.query(Progress).filter_by(student_id=current_user["id"]).all()


@router.get("/student/{student_id}", response_model=list[ProgressOut])
def list_progress_of_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("trainer")),
):
    return db.query(Progress).filter_by(student_id=student_id).all()
