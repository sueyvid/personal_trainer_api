# app/schemas/progress.py

from pydantic import BaseModel
from datetime import date

class ProgressBase(BaseModel):
    workout_id: int
    date: date

class ProgressCreate(ProgressBase):
    pass

class ProgressOut(ProgressBase):
    id: int
    student_id: int

    class Config:
        from_attributes = True
