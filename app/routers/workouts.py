# app/routers/workouts.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_role
from app.models.workout import Workout
from app.models.user import User
from app.schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutOut

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/", response_model=WorkoutOut, status_code=status.HTTP_201_CREATED)
def create_workout(
    data: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("trainer")),
):
    student_user = db.query(User).filter(User.id == data.student_id).first()
    if not student_user:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    workout = Workout(**data.dict(), trainer_id=current_user["id"])
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


@router.get("/", response_model=list[WorkoutOut])
def list_workouts_for_trainer(
    db: Session = Depends(get_db), current_user: dict = Depends(require_role("trainer"))
):
    return db.query(Workout).filter(Workout.trainer_id == current_user["id"]).all()


@router.get("/me", response_model=list[WorkoutOut])
def get_my_workouts_as_student(
    db: Session = Depends(get_db), current_user: dict = Depends(require_role("student"))
):
    workouts = db.query(Workout).filter(Workout.student_id == current_user["id"]).all()
    return workouts


@router.put("/{workout_id}", response_model=WorkoutOut)
def update_workout(
    workout_id: int,
    data: WorkoutUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("trainer")),
):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Treino não encontrado.")

    if workout.trainer_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: você não é o dono deste treino.",
        )

    for field, value in data.dict(exclude_unset=True).items():
        setattr(workout, field, value)

    db.commit()
    db.refresh(workout)
    return workout


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("trainer")),
):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Treino não encontrado.")

    if workout.trainer_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: você não é o dono deste treino.",
        )

    db.delete(workout)
    db.commit()
    return
