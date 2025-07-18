# app/models/progress.py

from sqlalchemy import Column, Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    date = Column(Date, nullable=False)

    # Evita duplicação de marcações no mesmo dia
    __table_args__ = (UniqueConstraint("student_id", "workout_id", "date", name="uq_progress_entry"),)

    student = relationship("User")
    workout = relationship("Workout")
