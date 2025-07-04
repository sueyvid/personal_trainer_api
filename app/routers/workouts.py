from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# ✅ 1. Mantém a sua importação centralizada, que é a correta.
from app.core.dependencies import get_db, require_role
from app.models.workout import Workout
from app.models.user import User
from app.schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutOut

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/", response_model=WorkoutOut)
def create_workout(
    data: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("trainer")),
):
    # ✅ 2. Adiciona uma busca pelo ID do treinador, tornando a lógica robusta.
    trainer_db = (
        db.query(User).filter(User.username == current_user["username"]).first()
    )
    if not trainer_db:
        raise HTTPException(
            status_code=404, detail="Treinador não encontrado no banco de dados."
        )

    student_user = db.query(User).filter(User.id == data.student_id).first()
    if not student_user:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    workout = Workout(**data.dict(), trainer_id=trainer_db.id)
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


# ✅ 3. Inclui a rota para listar treinos da branch main.
@router.get("/", response_model=list[WorkoutOut])
def list_workouts_for_trainer(
    db: Session = Depends(get_db), current_user: dict = Depends(require_role("trainer"))
):
    trainer_db = (
        db.query(User).filter(User.username == current_user["username"]).first()
    )
    if not trainer_db:
        raise HTTPException(status_code=404, detail="Treinador não encontrado.")

    return db.query(Workout).filter(Workout.trainer_id == trainer_db.id).all()


# ✅ 4. Inclui a rota para o aluno ver seus próprios treinos.
@router.get("/me", response_model=list[WorkoutOut])
def get_my_workouts_as_student(
    db: Session = Depends(get_db), current_user: dict = Depends(require_role("student"))
):
    student_db = (
        db.query(User).filter(User.username == current_user["username"]).first()
    )
    if not student_db:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    workouts = db.query(Workout).filter(Workout.student_id == student_db.id).all()
    return workouts


# ✅ 5. Inclui as rotas de update e delete.
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

    # Lógica para verificar se o treinador é o dono do treino pode ser adicionada aqui

    for field, value in data.dict(exclude_unset=True).items():
        setattr(workout, field, value)

    db.commit()
    db.refresh(workout)
    return workout


@router.delete("/{workout_id}", status_code=204)
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("trainer")),
):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Treino não encontrado.")

    db.delete(workout)
    db.commit()
    return {"message": "Treino excluído com sucesso."}
