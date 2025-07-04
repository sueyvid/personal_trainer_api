# app/models/__init__.py

from .user import User
from .workout import Workout

# ✅ Adicione esta linha para exportar os modelos e silenciar o erro F401
__all__ = ["User", "Workout"]
