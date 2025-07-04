# tests/test_auth.py

from fastapi.testclient import TestClient


def test_login_sucesso(client: TestClient):
    """
    Testa o login com um usuário e senha válidos.
    """
    # Arrange: Cria um usuário com um papel VÁLIDO.
    user_data = {"username": "testuser", "password": "testpassword", "role": "student"}
    response_register = client.post("/auth/register", json=user_data)
    assert response_register.status_code == 200

    # Act: Tenta fazer o login com as credenciais corretas.
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/auth/login", json=login_data)

    # Assert: Verifica se a resposta está correta.
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_senha_incorreta(client: TestClient):
    """
    Testa o login com uma senha incorreta.
    """
    # Arrange: Cria um usuário com um papel VÁLIDO.
    user_data = {
        "username": "testuser2",
        "password": "correctpassword",
        "role": "trainer",
    }
    response_register = client.post("/auth/register", json=user_data)
    assert response_register.status_code == 200  # Boa prática

    # Act: Tenta fazer o login com a senha errada.
    login_data = {"username": "testuser2", "password": "wrongpassword"}
    response = client.post("/auth/login", json=login_data)

    # Assert: Verifica se a API retorna o erro esperado (401 Unauthorized).
    assert response.status_code == 401
    assert response.json() == {"detail": "Usuário ou senha inválidos"}


def test_login_usuario_nao_existe(client: TestClient):
    """
    Testa o login com um usuário que não está cadastrado.
    """
    # Arrange: Não há usuário no banco de dados.

    # Act: Tenta fazer o login.
    login_data = {"username": "nonexistentuser", "password": "somepassword"}
    response = client.post("/auth/login", json=login_data)

    # Assert: Verifica se a API retorna o erro esperado (401 Unauthorized).
    assert response.status_code == 401
    assert response.json() == {"detail": "Usuário ou senha inválidos"}
