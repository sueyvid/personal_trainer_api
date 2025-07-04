# app/models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ex: "student", "trainer"

    # ✅ Mantém a sua estrutura de relacionamentos, que é a correta e mais completa.
    # Lista de treinos que este usuário (como treinador) criou
    created_workouts = relationship(
        "Workout",
        foreign_keys="[Workout.trainer_id]",
        back_populates="trainer",
        cascade="all, delete-orphan",
    )
    # Lista de treinos atribuídos a este usuário (como aluno)
    assigned_workouts = relationship(
        "Workout",
        foreign_keys="[Workout.student_id]",
        back_populates="student",
        cascade="all, delete-orphan",
    )
