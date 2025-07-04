import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from jose import JWTError

# As funções que queremos testar
from app.core.dependencies import get_current_user, require_role

# ... (seus testes existentes para get_current_user estão aqui) ...


# --- Novos Testes para require_role ---

def test_require_role_sucesso():
    """
    Testa se a dependência permite o acesso quando o papel do usuário é o correto.
    """
    # 1. Arrange
    # Cria uma instância da dependência que exige o papel "trainer"
    trainer_only_dependency = require_role("trainer")
    
    # Cria um usuário falso que satisfaz a condição
    fake_trainer_user = {"username": "test.trainer", "role": "trainer", "id": 123}

    # 2. Act
    # Chamamos a dependência diretamente, passando o usuário falso
    result = trainer_only_dependency(user=fake_trainer_user)

    # 3. Assert
    # O resultado deve ser o próprio usuário, indicando que a verificação passou
    assert result == fake_trainer_user


def test_require_role_falha_papel_incorreto():
    """
    Testa se a dependência levanta uma HTTPException 403 quando o papel é incorreto.
    """
    # 1. Arrange
    # Cria uma instância da dependência que exige o papel "trainer"
    trainer_only_dependency = require_role("trainer")
    
    # Cria um usuário falso que NÃO satisfaz a condição (ele é um "student")
    fake_student_user = {"username": "test.student", "role": "student", "id": 456}

    # 2. Act & 3. Assert
    # Usamos pytest.raises para verificar se a exceção correta é levantada
    with pytest.raises(HTTPException) as exc_info:
        trainer_only_dependency(user=fake_student_user)

    # Verificamos os detalhes da exceção capturada
    assert exc_info.value.status_code == 403
    assert "Acesso negado" in exc_info.value.detail