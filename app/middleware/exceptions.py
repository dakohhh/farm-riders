import aiohttp
from typing import Union
from fastapi.exceptions import RequestValidationError
from mongoengine.errors import NotUniqueError, ValidationError
from pymongo.errors import DuplicateKeyError
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


def handle_client_request_exceptions(app: FastAPI):

    @app.exception_handler(aiohttp.ClientResponseError)
    async def client_response_handler(request: Request, exc: aiohttp.ClientResponseError):

        return CustomResponse(message=exc.message, status=exc.status, success=False)


def configure_error_middleware(app: FastAPI):

    app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(BadRequestException, bad_request_exception_handler)
    app.add_exception_handler(ForbiddenException, forbidden_exception_handler)

    handle_client_request_exceptions(app)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return CustomResponse(message=exc.detail, status=exc.status_code, success=False)

    @app.exception_handler(DuplicateKeyError)
    async def mongo_duplicate_key_error_handler(request: Request, exc: DuplicateKeyError):
        if exc.details:

            field: Union[str, None] = None

            key_pattern: Union[dict, None] = exc.details.get('keyPattern', None)

            field: Union[str, None] = str(list(key_pattern.keys())[0]) if key_pattern else None

            if "_" in field:
                field = field.replace("_", " ")

        message = "{} already exists".format(field.capitalize())

        return CustomResponse(message=message, status=status.HTTP_400_BAD_REQUEST, success=False)

    @app.exception_handler(ValidationError)
    async def mongo_validation_error_handler(request: Request, exc: ValidationError):

        message = exc.message

        if exc.errors:

            key_error_fields = list(exc.errors.keys())

            if 'role' in key_error_fields:
                from ..enums.user import UserRoles

                message = f"role must be one of these: {[e.value for e in UserRoles]}"

        return CustomResponse(message=message, status=status.HTTP_400_BAD_REQUEST, success=False)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Extract the details from the exception
        errors = exc.errors()

        # Create a custom message format
        detail = []
        message: Union[str, None] = None
        for error in errors:
            field = error.get("loc", ["unknown"])[-1]  # Get the field name from the location
            if error.get("type") == "missing":
                message = f"Field '{field}' is required"

            elif error.get("type") == "value_error":

                if "_" in field:
                    field = field.replace("_", " ")
                message = f"{field} is invalid"

            elif error.get("type") == "string_type":

                if "_" in field:
                    field = field.replace("_", " ")
                message = f"{field} is invalid"

            elif error.get("type") == "enum":
                if "_" in field:
                    field = field.replace("_", " ")

                message = f"{field} is invalid"
                if field == "gender":
                    from ..enums.user import UserGender

                    message = f"gender must be one of these: {[e.value for e in UserGender]}"

            else:
                detail.append(
                    {
                        "type": error.get("type"),
                        "loc": error.get("loc"),
                        "msg": f"Invalid value for '{field}'",
                        "input": error.get("input"),
                    }
                )

        # Print the details if it's an unhandled error
        print(detail)

        return CustomResponse(message=message, status=status.HTTP_400_BAD_REQUEST, success=False)

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return CustomResponse(
            message="Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False
        )

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return CustomResponse(message=str(exc.detail), status=status.HTTP_429_TOO_MANY_REQUESTS, success=False)
