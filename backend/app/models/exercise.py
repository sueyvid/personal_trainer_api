# app/models/exercise.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    reps = Column(String)  # Ex: "3x12", "4x10", etc.
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)

    workout = relationship("Workout", back_populates="exercises")
