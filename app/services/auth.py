from fastapi import APIRouter
from ..models.user import User
from ..models.profile import Profile, DriverProfile
from ..schema.auth import CreateUser, Login
from ..utils.hashing import hashPassword, checkPassword
from ..services.token import TokenService
from ..utils.exceptions import BadRequestException


class AuthService:

    @staticmethod
    async def register(create_user: CreateUser):

        hashed_password = hashPassword(create_user.password)

        create_user_dict = create_user.model_dump(exclude={"password"})

        create_user_dict.update({"password": hashed_password})

        user_collection = User._get_collection()

        user = user_collection.insert_one(create_user_dict)

        if create_user.role == "driver":
            DriverProfile(user=user.inserted_id).save()
        else:
            Profile(user=user.inserted_id).save()

        cleaned_phone_number = create_user.phone_number.replace('tel:', '').replace('-', '')

        # Send Verification Mail

        result = {
            'user': {
                'user_id': str(user.inserted_id),
                'has_completed_profile': False,
                'phone_number': cleaned_phone_number,
                'role': create_user.role,
            }
        }

        return result

    @staticmethod
    async def login(login: Login):

        if login.email:
            user = User.objects.filter(email=login.email).first()
        elif login.phone_number:
            user: User = User.objects.filter(phone_number=login.phone_number).first()

        if not user:
            raise BadRequestException("incorrect email or password")

        valid_password: bool = checkPassword(login.password, user.password)

        if not valid_password:
            raise BadRequestException("incorrect email or password")

        token = await TokenService.generate_auth_token(user)

        return {"role": user.role.value, "has_completed_profile": user.has_completed_profile, "token": token}
