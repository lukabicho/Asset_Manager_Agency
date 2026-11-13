"""Security utilities for Argon2 password hashing and JWT token management."""
from datetime import datetime, timedelta, UTC
import uuid
import jwt
from pwdlib import PasswordHash
from app.core.config import settings

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Hash a password using argon2)."""
    return password_hash.hash(password)

def verify_password(verifiable_password: str, hashed_password: str) -> bool:
    """Verify a password against a stored hashed password."""
    return password_hash.verify(verifiable_password, hashed_password)

def create_token(subject: str, token_type: str, expires_delta: timedelta):
    """Create a signed JWT access or refresh token with a unique JTI."""
    now = datetime.now(UTC)
    payload = {
        "sub": subject,
        "type": token_type,
        "jti": str(uuid.uuid4()),
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_access_token(user_id: str):
    """Create an access token using JWT."""
    return create_token(subject=user_id, token_type="access", expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(user_id: str):
    """Create a refresh token using JWT."""
    return create_token(subject=user_id, token_type="refresh", expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

def decode_token(token: str):
    """Decode a JWT access token."""
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

