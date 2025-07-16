from src.services.auth import AuthService


def testcreate_access_token_existence():
    data = {"user_id": 1}
    jwt_token = AuthService().create_access_token(data)
    assert jwt_token
    assert isinstance(jwt_token, str)
