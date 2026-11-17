"""This module provides the stateless UserManager service that's responsible
for querying, registering, and authenticating users from a DataBase"""
import uuid
from sqlalchemy import or_,select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.exceptions import UserAlreadyExistsError

class UserManager:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        """Fetches Emails from the database"""
        statement = select(User).where(User.email == email)
        return self.db.scalars(statement).first()

    def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        """Fetches Users from the database"""
        statement = select(User).where(User.id == user_id)
        return self.db.scalars(statement).first()

    def create_user(self, user_create: UserCreate) -> User:
        """Creates a new user if the user doesn't exist"""
        if self.get_user_by_email(user_create.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="This email is already used")

        db_user = User(email = user_create.email, username = user_create.username, password = hash_password(user_create.password))
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate_user(self, username_or_email: str, password: str) -> User | None:
        """Checks if the user exists in the database"""
        statement = select(User).where(or_(User.email == username_or_email, User.username == username_or_email))
        user = self.db.scalars(statement).first()
        if not user or not verify_password(password, user.password):
            return None
        return user