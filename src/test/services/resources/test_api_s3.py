from unittest.mock import patch

import jwt
from src.services.resources.api_s3 import decode_jwt, retrieve_user


def test_decode_jwt_valid_token():
    # Simulando um token JWT válido
    token = jwt.encode({"id": "user123"}, "secret", algorithm="HS256")

    user_id = decode_jwt(token)

    assert user_id == "user123"


def test_decode_jwt_invalid_token():
    invalid_token = "invalid.token"

    response = decode_jwt(invalid_token)

    assert response[1] == 401  # Código de erro 401 para token inválido


@patch("src.services.resources.api_s3.requests.get")
def test_retrieve_user_success(mock_get):
    # Mockando a resposta da API de usuários
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"id": "user123", "name": "John Doe"}

    user = retrieve_user("user123")

    assert user == {"id": "user123", "name": "John Doe"}
