from fastapi import APIRouter
from ..schema.user import UserProfile
router = APIRouter(prefix="/user", tags=["Vendor"])


@router.patch("/profile")
async def update_user_profile(profile: UserProfile):
    return {"message": "Profile"}
