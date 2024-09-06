from fastapi import APIRouter, Request, status
from ..schema.auth import CreateUser, Login
from ..services.auth import AuthService
from ..utils.response import CustomResponse


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(login: Login):

    result = await AuthService.login(login)

    return CustomResponse("login successful", data=result)


@router.post("/register")
async def register(request: Request, create_user: CreateUser):

    result = await AuthService.register(create_user)

    return CustomResponse("register user successful", data=result, status=status.HTTP_201_CREATED)


@router.get("/forgot-password")
async def forgot_password():
    return {"message": "Forgot Password"}


@router.get("/reset-password")
async def reset_password():
    return {"message": "Reset Password"}


@router.get("/logout")
async def logout():
    return {"message": "Logout"}


@router.get("/verify-email")
async def verify_email():
    return {"message": "Verify Email"}


@router.get("/resend-verification-email")
async def resend_verification_email():
    return {"message": "Resend Verification Email"}


@router.get("/change-password")
async def change_password():
    return {"message": "Change Password"}


@router.get("/update-profile")
async def update_profile():
    return {"message": "Update Profile"}


@router.get("/delete-account")
async def delete_account():
    return {"message": "Delete Account"}
