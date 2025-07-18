# app/routers/workouts.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_role
from app.models.workout import Workout
from app.models.user import User
from app.schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutOut, WorkoutAssign


router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/", response_model=WorkoutOut, status_code=status.HTTP_201_CREATED)
def create_workout(
    data: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("trainer")),
):
    workout = Workout(
        name=data.name,
        description=data.description,
        start_date=data.start_date,
        end_date=data.end_date,
        trainer_id=current_user["id"],
    )
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
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("student")),
):
    user = db.query(User).filter(User.id == current_user["id"]).first()
    return user.assigned_workouts  # <-- pega os treinos atribuídos ao aluno



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

@router.patch("/{workout_id}/assign", response_model=WorkoutOut)
def assign_students_to_workout(
    workout_id: int,
    data: WorkoutAssign,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("trainer")),
):
    workout = db.query(Workout).filter_by(id=workout_id).first()

    if not workout or workout.trainer_id != current_user["id"]:
        raise HTTPException(status_code=404, detail="Treino não encontrado ou acesso negado")

    students = db.query(User).filter(User.id.in_(data.student_ids)).all()
    if len(students) != len(data.student_ids):
        raise HTTPException(status_code=400, detail="Um ou mais alunos não existem")
    
    for student in students:
        if student not in workout.students:
            workout.students.append(student)
            
    db.commit()
    db.refresh(workout)
    return workout

@router.delete("/{workout_id}/unassign/{student_id}", status_code=204)
def unassign_student_from_workout(
    workout_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("trainer")),
):
    workout = db.query(Workout).filter_by(id=workout_id).first()

    if not workout or workout.trainer_id != current_user["id"]:
        raise HTTPException(status_code=404, detail="Treino não encontrado ou acesso negado")

    student = db.query(User).filter_by(id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    if student in workout.students:
        workout.students.remove(student)
        db.commit()
    return
