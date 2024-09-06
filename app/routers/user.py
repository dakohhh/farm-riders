from fastapi import APIRouter, Depends
from ..middleware.auth import Auth
from ..enums.user import UserRoles
from ..models.user import User
from ..schema.user import UserProfile
router = APIRouter(prefix="/user", tags=["Vendor"])


@router.patch("/profile")
async def update_user_profile(profile: UserProfile, user: User = Depends(Auth())):

    print(user.id)
    return {"message": "Profile"}
