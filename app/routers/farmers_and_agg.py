from fastapi import APIRouter, Request, Depends
from pymongo.collection import Collection
from ..services.user import UserService

from ..utils.response import CustomResponse
from ..enums.user import UserRoles
from ..middleware.auth import Auth
from ..models.user import User
from ..models.profile import Profile
from ..schema.user import UserProfile, DriverProfile

router = APIRouter(prefix="/user", tags=["FARMERS AND AGGREGATORS"])





