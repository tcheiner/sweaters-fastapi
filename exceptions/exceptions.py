# exceptions.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class UserNotFoundException(Exception):
    """Custom exception for when a user is not found."""
    def __init__(self, message: str, endpoint: str = None, function: str = None):
        self.message = message
        self.endpoint = endpoint
        self.function = function
        super().__init__(self.message)

    def __str__(self):
        base_msg = f"{self.message}"
        if self.endpoint:
            base_msg += f" (endpoint: {self.endpoint})"
        if self.function:
            base_msg += f" (function: {self.function})"
        return base_msg

class UserAlreadyExistsException(Exception):
    """Custom exception for when a user already exists."""
    def __init__(self, message: str, endpoint: str = None, function: str = None):
        self.message = message
        self.endpoint = endpoint
        self.function = function
        super().__init__(self.message)

    def __str__(self):
        base_msg = f"{self.message}"
        if self.endpoint:
            base_msg += f" (endpoint: {self.endpoint})"
        if self.function:
            base_msg += f" (function: {self.function})"
        return base_msg

class GameNotFoundException(Exception):
    """Custom exception for when a game is not found."""
    def __init__(self, message: str, endpoint: str = None, function: str = None):
        self.message = message
        self.endpoint = endpoint
        self.function = function
        super().__init__(self.message)

    def __str__(self):
        base_msg = f"{self.message}"
        if self.endpoint:
            base_msg += f" (endpoint: {self.endpoint})"
        if self.function:
            base_msg += f" (function: {self.function})"
        return base_msg

class InvalidUserException(Exception):
    """Custom exception for when a user is invalid."""
    def __init__(self, message: str, endpoint: str = None, function: str = None):
        self.message = message
        self.endpoint = endpoint
        self.function = function
        super().__init__(self.message)

    def __str__(self):
        base_msg = f"{self.message}"
        if self.endpoint:
            base_msg += f" (endpoint: {self.endpoint})"
        if self.function:
            base_msg += f" (function: {self.function})"
        return base_msg

class UnexpectedException(Exception):
    """Custom exception for when a user is invalid."""

    def __init__(self, message: str, endpoint: str = None, function: str = None):
        self.message = message
        self.endpoint = endpoint
        self.function = function
        super().__init__(self.message)

    def __str__(self):
        base_msg = f"{self.message}"
        if self.endpoint:
            base_msg += f" (endpoint: {self.endpoint})"
        if self.function:
            base_msg += f" (function: {self.function})"
        return base_msg

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(UserNotFoundException)
    async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "detail": str(exc),
                "endpoint": exc.endpoint,
                "function": exc.function
            }
        )
        
    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_exception_handler(request: Request, exc: UserAlreadyExistsException):
        return JSONResponse(
            status_code=409,
            content={
                "detail": str(exc),
                "endpoint": exc.endpoint,
                "function": exc.function
            }
        )
        
    @app.exception_handler(GameNotFoundException)
    async def game_not_found_exception_handler(request: Request, exc: GameNotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "detail": str(exc),
                "endpoint": exc.endpoint,
                "function": exc.function
            }
        )
        
    @app.exception_handler(InvalidUserException)
    async def invalid_user_exception_handler(request: Request, exc: InvalidUserException):
        return JSONResponse(
            status_code=400,
            content={
                "detail": str(exc),
                "endpoint": exc.endpoint,
                "function": exc.function
            }
        )
