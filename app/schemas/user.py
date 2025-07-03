from pydantic import BaseModel
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

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str
