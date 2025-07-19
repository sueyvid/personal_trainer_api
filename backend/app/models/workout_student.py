# app/models/workout_student.py

from sqlalchemy import Column, Integer, ForeignKey, Table
from app.core.database import Base

# Tabela de associação (aluno <-> treino)

workout_student = Table(
    "workout_student",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("workout_id", Integer, ForeignKey("workouts.id"), primary_key=True),
)
