from pydantic import BaseModel
from datetime import date
from typing import Optional

class WorkoutBase(BaseModel):
    name: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]

class WorkoutCreate(WorkoutBase):
    aluno_id: int

class WorkoutUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    
class WorkoutOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    aluno_id: int

    model_config = {"from_attributes": True}
