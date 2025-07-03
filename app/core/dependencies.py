from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM

# define o esquema de segurança usando HTTPBearer
bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials  # extrai o token do Authorization header
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def require_role(required_role: str):
    def role_dependency(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado, requer papel '{required_role}'"
            )
        return user
    return role_dependency
