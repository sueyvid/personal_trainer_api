# tests/unit/test_dependencies.py

import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from jose import JWTError

# A função que queremos testar
from app.core.dependencies import get_current_user, require_role


def test_get_current_user_sucesso():
    """
    Testa o caminho feliz: um token válido é decodificado e o usuário é retornado.
    """
    # 1. Arrange: Prepara um payload de usuário simulado
    user_payload = {"sub": "testuser", "role": "student", "id": 1}

    # Simula as credenciais que a função recebe
    mock_credentials = MagicMock()
    mock_credentials.credentials = "um.token.jwt.falso"

    # 2. Act & Mock: Substitui jwt.decode por um mock que retorna nosso payload
    # O decorator @patch faz a mágica de substituir a função real durante o teste.
    with patch("app.core.dependencies.jwt.decode") as mock_jwt_decode:
        # Configuramos o que o mock deve retornar quando for chamado
        mock_jwt_decode.return_value = user_payload

        # Chamamos a função a ser testada
        user = get_current_user(credentials=mock_credentials)

    # 3. Assert: Verifica se a função se comportou como esperado
    # Garante que a função de decodificação foi chamada com os parâmetros corretos
    mock_jwt_decode.assert_called_once()
    # Garante que o usuário retornado é o que nosso mock forneceu
    assert user == {"username": "testuser", "role": "student", "id": 1}


def test_get_current_user_falha_token_invalido():
    """
    Testa o caminho de falha: o token causa um JWTError.
    """
    # 1. Arrange: Simula as credenciais
    mock_credentials = MagicMock()
    mock_credentials.credentials = "um.token.jwt.invalido"

    # 2. Act & Mock: Substitui jwt.decode por um mock que levanta um erro
    with patch("app.core.dependencies.jwt.decode") as mock_jwt_decode:
        # Configuramos o mock para simular um erro de decodificação
        mock_jwt_decode.side_effect = JWTError("Token could not be validated")

        # 3. Assert: Verifica se a exceção HTTP correta foi levantada
        # pytest.raises é um gerenciador de contexto que captura a exceção
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials=mock_credentials)

        # Verifica os detalhes da exceção
        assert exc_info.value.status_code == 401
        assert "Token inválido" in exc_info.value.detail


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
