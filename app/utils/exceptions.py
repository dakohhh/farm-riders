from fastapi import Request, status
from fastapi.responses import JSONResponse
from .response import CustomResponse
from slowapi.errors import RateLimitExceeded


class UnauthorizedException(Exception):
    def __init__(self, message: str):
        self.message = message


async def unauthorized_exception_handler(request: Request, exception: UnauthorizedException):

    return CustomResponse(exception.message, status.HTTP_401_UNAUTHORIZED, success=False)


class NotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message


async def not_found_exception_handler(request: Request, exception: NotFoundException):

    return CustomResponse(exception.message, status.HTTP_404_NOT_FOUND, success=False)


class ForbiddenException(Exception):
    def __init__(self, message: str):
        self.message = message


async def forbidden_exception_handler(request: Request, exception: ForbiddenException):

    return CustomResponse(exception.message, status.HTTP_403_FORBIDDEN, success=False)


class BadRequestException(Exception):
    def __init__(self, message: str):
        self.message = message


async def bad_request_exception_handler(request: Request, exception: BadRequestException):

    return CustomResponse(exception.message, status.HTTP_400_BAD_REQUEST, success=False)


async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"status": status.HTTP_429_TOO_MANY_REQUESTS, "message": str(exc.detail), "success": False},
    )
