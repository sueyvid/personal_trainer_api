from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum

# O Enum para os papéis está correto.
class UserRole(str, Enum):
    student = "student"
    trainer = "trainer"

# --- Schema Base ---
class UserBase(BaseModel):
    username: str

# --- Schema para Login ---
# ✅ NOVO: Schema dedicado exclusivamente para a rota de login.
class UserLogin(UserBase):
    password: str

# --- Schema para Criação de Usuário ---
# ✅ ATUALIZADO: Herda de UserLogin para não repetir código.
class UserCreate(UserLogin):
    role: UserRole

# --- Schema para Respostas (saída de dados) ---
class UserOut(UserBase):
    id: int
    role: UserRole
    # ✅ ATUALIZADO: Usando ConfigDict para compatibilidade com Pydantic V2
    model_config = ConfigDict(from_attributes=True)

# --- Schema para Atualização de Usuário ---
class UserUpdate(BaseModel):
    # Opcional foi removido pois a rota de atualização espera um novo valor
    password: str

# --- Schema para o Token JWT ---
class Token(BaseModel):
    access_token: str
    token_type: str