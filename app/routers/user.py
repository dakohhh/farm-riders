from fastapi import APIRouter, Depends
from ..middleware.auth import Auth
from ..enums.user import UserRoles
from ..schema.user import UserProfile
router = APIRouter(prefix="/user", tags=["Vendor"])


@router.patch("/profile")
async def update_user_profile(profile: UserProfile, user = Depends(Auth())):
    return {"message": "Profile"}
