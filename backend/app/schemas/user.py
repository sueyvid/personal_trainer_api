from pydantic import BaseModel, ConfigDict
from enum import Enum


class UserRole(str, Enum):
    student = "student"
    trainer = "trainer"


class UserBase(BaseModel):
    username: str


class UserLogin(UserBase):
    password: str


class UserCreate(UserLogin):
    role: UserRole


class UserOut(UserBase):
    id: int
    role: UserRole
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    password: str


class UserDelete(BaseModel):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
