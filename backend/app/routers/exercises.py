# app/routers/exercises.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_role
from app.models.exercise import Exercise
from app.models.workout import Workout
from app.schemas.exercise import ExerciseCreate, ExerciseOut

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.post("/", response_model=ExerciseOut)
def create_exercise(
    data: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("trainer")),
):
    # Valida se o treino é do treinador
    workout = (
        db.query(Workout)
        .filter(Workout.id == data.workout_id, Workout.trainer_id == current_user["id"])
        .first()
    )

    if not workout:
        raise HTTPException(
            status_code=403, detail="Você não pode adicionar exercícios a esse treino."
        )

    exercise = Exercise(**data.dict())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


@router.get("/workout/{workout_id}", response_model=list[ExerciseOut])
def list_exercises_for_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_db),  # qualquer usuário pode ver
):
    exercises = db.query(Exercise).filter(Exercise.workout_id == workout_id).all()
    return exercises
