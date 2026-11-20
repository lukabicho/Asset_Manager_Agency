"""This module contains FastAPI dependencies for DataBases, managers and authentication."""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import uuid
import jwt

from app.database.session import SessionLocal
from app.core.security import decode_token
from app.managers.user_manager import UserManager
from app.core.exceptions import InvalidCredentialsError
from app.managers.redis_manager import RedisManager
from app.managers.agency_manager import AgencyManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db():
    """Provides a database connection"""
    with SessionLocal() as db:
        try:
            yield db
        except Exception:
            db.rollback()
            raise

def get_user_manager(db: Session = Depends(get_db)): #Depends() is a fastapi class that ensures that get_db gets passed though. if get_db() fails, the function is not executed
    """Provides UserManager class from managers/user_manager with a database session"""
    return UserManager(db=db)

def get_current_user(token: str = Depends(oauth2_scheme), user_manager: UserManager = Depends(get_user_manager)):
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise InvalidCredentialsError("Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise InvalidCredentialsError("Token missing subject")

        parsed_id = uuid.UUID(user_id)
    except(jwt.PyJWTError, ValueError):
        raise InvalidCredentialsError("Invalid token Credentials")

    user = user_manager.get_user_by_id(parsed_id)
    if not user or not user.is_active:
        raise InvalidCredentialsError("User not found")

    return user

def get_redis_manager():
    return RedisManager()

def get_agency_manager(db: Session = Depends(get_db)):
    return AgencyManager(db)