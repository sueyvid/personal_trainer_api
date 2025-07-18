# app/models/workout.py

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.workout_student import workout_student


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    trainer_id = Column(Integer, ForeignKey("users.id"))

    # Isso é crucial para o SQLAlchemy entender as múltiplas conexões com a tabela User.
    trainer = relationship(
        "User", foreign_keys=[trainer_id], back_populates="created_workouts"
    )
    exercises = relationship(
        "Exercise", back_populates="workout", cascade="all, delete-orphan"
    )
    students = relationship(
        "User",
        secondary=workout_student,
        back_populates="assigned_workouts",
    )


