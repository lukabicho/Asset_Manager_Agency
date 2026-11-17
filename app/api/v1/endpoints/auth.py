from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timezone
import uuid

from app.api.deps import get_current_user, get_user_manager, get_redis_manager
from app.schemas.user import UserResponse, UserCreate, TokenResponse
from app.core.exceptions import InvalidCredentialsError
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.managers.user_manager import UserManager
from app.managers.redis_manager import RedisManager
from app.core.exceptions import UserNotFoundError
from app.schemas.user import RefreshTokenRequest
from app.models.user import User


router = APIRouter(prefix="/auth", tags=["authentication"])

def _validate_and_revoke_refresh_token(refresh_token: str, redis_manager: RedisManager):
    """Validates that the refresh token is valid and revoke it"""
    try:
        payload = decode_token(refresh_token)
    except jwt.PyJWTError:
        raise InvalidCredentialsError("Invalid refresh token")

    if payload.get("type") != "refresh":
        raise InvalidCredentialsError("Invalid refresh token type")

    jti = payload.get("jti")
    user_id = payload.get("sub")
    exp = payload.get("exp")

    if not jti or not user_id or not exp:
        raise InvalidCredentialsError("Malformed refresh token")

    if redis_manager.is_blacklisted(jti):
        raise InvalidCredentialsError("Refresh token is already revoked")

    remaining_second = int(exp - datetime.now(timezone.utc).timestamp())
    redis_manager.blacklist_token(jti, remaining_second)

    return user_id

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
        user_config: UserCreate,
        user_manager: UserManager = Depends(get_user_manager),
):
    """Register a new user"""
    return user_manager.create_user(user_config)

@router.post("/login", response_model = TokenResponse)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_manager: UserManager = Depends(get_user_manager),
):
    """Oauth2 compatible authentication flow"""
    user = user_manager.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise InvalidCredentialsError("Incorrect email/username or password")

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id))
    )

@router.get("/me", response_model=UserResponse)
def me(current_user: UserManager = Depends(get_current_user)):
    """Returns the current authenticated user"""
    return current_user

@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshTokenRequest, user_manager: UserManager = Depends(get_user_manager), redis_manager: RedisManager = Depends(get_redis_manager())):
    """Rotate a valid refresh token for a new access and refresh token pair."""
    user_id = _validate_and_revoke_refresh_token(body.refresh_token, redis_manager)

    user = user_manager.get_user_by_id(uuid.UUID(user_id))
    if not user or not user.is_active:
        raise UserNotFoundError("User does not exist")

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id))
    )

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(body: RefreshTokenRequest, current_user: User = Depends(get_current_user), redis_manager: RedisManager = Depends(get_redis_manager())):
    """Revoke the user's access and refresh token"""
    _validate_and_revoke_refresh_token(body.refresh_token, redis_manager)
    return None