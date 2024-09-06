import jwt
from datetime import datetime, timedelta
from ..utils.exceptions import ForbiddenException
from ..schema.token import TokenData
from ..settings import settings


class TokenService:

    @staticmethod
    async def verify_auth_token(token: str):

        try:

            decoded_token: dict = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

            expire_timestamp = decoded_token.get("expire")

            current_timestamp = int(datetime.now().timestamp())

            if current_timestamp > expire_timestamp:
                raise ForbiddenException("invalid Token, could not validate credentials")

            return TokenData(
                user_id=decoded_token.get["user_id"],
                expire=decoded_token.get("expire"),
            )

        except jwt.InvalidTokenError:

            raise ForbiddenException("Invalid Token, could not validate credentials")
        

    @staticmethod
    async def generate_auth_token(user):

        expire = (datetime.now() + timedelta(days=1)).timestamp()

        token_data = TokenData(user_id=str(user.id), expire=int(expire))

        token = jwt.encode(token_data.model_dump(), settings.JWT_SECRET, algorithm="HS256")

        return token