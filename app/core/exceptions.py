"""Exceptions module."""
class AppException(Exception):
    def __init__(self, message: str):
        """Base class for all exceptions."""
        self.message = message
        super().__init__(message)


class UserNotFoundError(AppException):
    """Raised when a user is not found."""
    pass

class UserAlreadyExistsError(AppException):
    """Raised when a user already exists."""
    pass

class InvalidCredentialsError(AppException):
    """Raised when an invalid credentials are passed and login fails."""
    pass

class AssetStorageError(AppException):
    """Raised when an asset storage error occurs."""
    pass