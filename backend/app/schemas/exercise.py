# app/schemas/exercise.py

from pydantic import BaseModel
from typing import Optional


class ExerciseBase(BaseModel):
    name: str
    description: Optional[str]
    reps: Optional[str]


class ExerciseCreate(ExerciseBase):
    workout_id: int


class ExerciseOut(ExerciseBase):
    id: int
    workout_id: int

    class Config:
        from_attributes = True
