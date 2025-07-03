from pydantic import BaseModel, constr
from typing import Optional
from app.models.user import UserRole
from enum import Enum

class UserRole(str, Enum):
    aluno = "student"
    treinador = "trainer"

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole


class UserOut(BaseModel):
    id: int
    username: str
    role: UserRole

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[constr(min_length=3)]
    password: Optional[constr(min_length=6)]

class UserDelete(BaseModel):
    password: constr(min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str
