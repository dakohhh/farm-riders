from typing import Any, List
from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..models.user import User
from ..utils.exceptions import ForbiddenException, BadRequestException
from typing import Union

from ..services.token import TokenService
from ..enums.user import UserRoles

bearer = HTTPBearer()


class Auth:
    def __init__(self, roles: Union[UserRoles, List[UserRoles]]) -> None:

        self.roles = roles if isinstance(roles, list) else [roles]

    async def __call__(self, request: Request, data: HTTPAuthorizationCredentials = Depends(bearer)) -> User:

        access_token_data = TokenService.verify_auth_token(data.credentials)

        user: Union[User, None] = User.objects.filter(id=access_token_data).first()

        if user is None:
            raise BadRequestException("-middleware/user-not-found")

        if user.role not in self.roles:
            raise ForbiddenException("-middleware/user-not-authorized")

        return user
