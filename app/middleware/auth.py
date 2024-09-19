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
    def __init__(self, roles: Union[UserRoles, List[UserRoles] | None] = None) -> None:

        self.roles = (roles if isinstance(roles, list) else [roles]) if roles else []

    async def __call__(self, request: Request, data: HTTPAuthorizationCredentials = Depends(bearer)) -> User:

        user_id = await TokenService.verify_auth_token(data.credentials)

        user: Union[User, None] = User.objects.filter(id=user_id).first()

        if user is None:
            raise BadRequestException("-middleware/user-not-found")

        if self.roles and (user.role not in self.roles):
            raise ForbiddenException("-middleware/user-not-authorized")

        # Add a Typed user here using pydantic Annotations

        return user
