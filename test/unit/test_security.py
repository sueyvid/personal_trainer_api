# tests/unit/test_security.py

from unittest.mock import patch
from datetime import datetime, timedelta
from jose import jwt

# A função que queremos testar
from app.core.security import create_access_token


def test_create_access_token():
    """
    Testa se o token é criado com os dados corretos no payload.
    """
    # 1. Arrange: Prepara os dados de entrada
    user_data = {"sub": "testuser", "role": "student", "id": 1}

    # 2. Act: Chama a função que está sendo testada
    token = create_access_token(data=user_data)

    # 3. Assert: Verifica se o resultado está correto
    # Decodificamos o token gerado para verificar seu conteúdo (payload)
    # Usamos as mesmas configurações que a função original deveria usar
    # NOTA: Para este teste funcionar, a SECRET_KEY e o ALGORITHM precisam
    # ser os mesmos que os definidos no seu app/core/config.py, ou você pode
    # mocká-los também se quiser um isolamento ainda maior.
    from app.core.config import settings

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert payload["sub"] == user_data["sub"]
    assert payload["role"] == user_data["role"]
    assert payload["id"] == user_data["id"]
    # Verifica se a data de expiração foi adicionada e é uma data no futuro
    assert "exp" in payload
    assert datetime.fromtimestamp(payload["exp"]) > datetime.now()
