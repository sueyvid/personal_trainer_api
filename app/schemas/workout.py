from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.schemas.exercise import ExerciseOut
from typing import List
from app.schemas.user import UserOut


class WorkoutBase(BaseModel):
    name: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]


class WorkoutOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    students: list[UserOut] = []
    model_config = {"from_attributes": True}

class WorkoutAssign(BaseModel):
    student_ids: list[int]
