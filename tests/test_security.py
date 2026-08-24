import pytest
from app.core.security import get_password_hash, verify_password, create_access_token
from app.auth.jwt import decode_token

def test_password_hashing():
    password = "SuperSecretPassword123!"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

@pytest.mark.asyncio
async def test_jwt_token_generation_and_decoding():
    user_id = "test-user-uuid-12345"
    token = create_access_token(subject=user_id)
    payload = await decode_token(token)
    assert payload.sub == user_id
    assert payload.type == "access"
