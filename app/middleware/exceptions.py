import json
from mongoengine.errors import NotUniqueError, ValidationError
from fastapi import FastAPI, Request, status
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException as StarletteHTTPException
from ..utils.response import CustomResponse

from ..utils.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    unauthorized_exception_handler,
    not_found_exception_handler,
    bad_request_exception_handler,
    forbidden_exception_handler,
)


def configure_error_middleware(app: FastAPI):

    app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(BadRequestException, bad_request_exception_handler)
    app.add_exception_handler(ForbiddenException, forbidden_exception_handler)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return CustomResponse(message=exc.detail, status=exc.status_code, success=False)

    @app.exception_handler(NotUniqueError)
    async def mongo_duplicate_key_error_handler(request: Request, exc: NotUniqueError):

        _args = exc.args[0]

        json_part = _args.split('full error: ')[1].replace("'", '"').split(", \"errmsg")[0] + '}'

        err = None
        try:
            error_details = json.loads(json_part)

            key_pattern = error_details.get('keyPattern', {})

            field: str | None = list(key_pattern.keys())[0] if key_pattern else None

            field = (field.replace("_", " ").capitalize() if "_" in field else field.capitalize()) if field else None

            err = f"{field} already exists"
        except json.JSONDecodeError:
            err = "already exists"

        return CustomResponse(message=err, status=status.HTTP_400_BAD_REQUEST, success=False)
    

    @app.exception_handler(ValidationError)
    async def mongo_validation_error_handler(request: Request, exc: ValidationError):

        key_error_fields = list(exc.errors.keys())
        
        message = exc.message

        if 'role' in key_error_fields:
            from ..enums.user import UserRoles

            message = f"role must be one of these: {[e.value for e in UserRoles]}"

        return CustomResponse(message=message, status=status.HTTP_400_BAD_REQUEST, success=False)
    


    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return CustomResponse(
            message="Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False
        )

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return CustomResponse(message=str(exc.detail), status=status.HTTP_429_TOO_MANY_REQUESTS, success=False)
