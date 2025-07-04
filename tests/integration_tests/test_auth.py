from src.services.auth import AuthService


def test_dencode_and_decode_access_token():
    data = {"user_id": 1}
    service = AuthService()
    
    jwt_token = service.create_access_token(data)
    payload = service.decode_access_token(jwt_token)
    
    assert payload
    assert payload["user_id"] == data["user_id"]
