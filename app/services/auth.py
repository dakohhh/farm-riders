from app.schema.token import TokenData
from ..models.user import User
from ..schema.auth import CreateUser, Login
from ..utils.hashing import hashPassword, checkPassword
from ..services.token import TokenService
from ..utils.exceptions import BadRequestException


class AuthService:

    @staticmethod
    async def register(create_user: CreateUser):

        hashed_password = hashPassword(create_user.password)

        create_user = create_user.model_dump(exclude={"password"})

        user = User(**create_user, password=hashed_password)

        user.save()

        # MailService.sendVerificationEmail(new_user, token);

        result = {
            'user': {
                'id': str(user.id),
                'firstname': user.firstname,
                'lastname': user.lastname,
                'email': user.email,
                'phone_number': user.phone_number,
                'role': user.role,
            }
        }

        return result

    @staticmethod
    async def login(login: Login):

        user = User.objects(email=login.email).first()

        if not user:
            raise BadRequestException("Invalid email or password")
        
        valid_password: bool = checkPassword(login.password, user.password)

        if not valid_password:
            raise BadRequestException("Invalid email or password")
        
        token = await TokenService.generate_auth_token(user)

        return {"role": user.role.value, "token": token}


        
