from sqlalchemy import Column, Integer, String, Enum
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    aluno = "student"
    treinador = "trainer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.aluno, nullable=False)
