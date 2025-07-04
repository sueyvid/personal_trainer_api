from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, require_role
from app.routers.auth import get_db
from app.models.workout import Workout
from app.models.user import User
from app.schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutOut

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"]
)

# criar treino (apenas treinador)
@router.post("/", response_model=WorkoutOut)
def create_workout(
    data: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("trainer"))
):
    aluno = db.query(User).filter(User.id == data.aluno_id).first()
    if not aluno:
        raise HTTPException(404, "Aluno não encontrado")
    
    workout = Workout(**data.dict())
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

# listar todos treinos do treinador
@router.get("/", response_model=list[WorkoutOut])
def list_workouts(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("trainer"))
):
    return db.query(Workout).all()

# editar treino
@router.put("/{workout_id}", response_model=WorkoutOut)
def update_workout(
    workout_id: int,
    data: WorkoutUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("trainer"))
):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(404, "Treino não encontrado")
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(workout, field, value)
    
    db.commit()
    db.refresh(workout)
    return workout

# excluir treino
@router.delete("/{workout_id}")
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("trainer"))
):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(404, "Treino não encontrado")
    db.delete(workout)
    db.commit()
    return {"message": "Treino excluído com sucesso"}

# Visualizar treinos do aluno
# router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.get("/me", response_model=list[WorkoutOut])
def get_my_workouts(
    db: Session = Depends(get_db),
    user=Depends(require_role("student"))
):
    workouts = db.query(Workout).filter(Workout.aluno_id == user["id"]).all()
    return workouts
