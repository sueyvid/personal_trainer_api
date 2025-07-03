from pydantic import BaseModel
from datetime import date
from typing import Optional

class WorkoutBase(BaseModel):
    title: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]

class WorkoutCreate(WorkoutBase):
    aluno_id: int

class WorkoutUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]

class WorkoutOut(WorkoutBase):
    id: int
    aluno_id: int

    model_config = {"from_attributes": True}
