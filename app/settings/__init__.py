import os
import certifi
from enum import Enum
from pathlib import Path
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


DEPLOYMENT_ENV = os.getenv("PYTHON_ENV")

BASE_DIR = Path(__file__).resolve().parent.parent

CERTIFICATE = os.path.join(os.path.dirname(certifi.__file__), "cacert.pem")

# Path to .env file
DOTENV = os.path.join(BASE_DIR, ".env")


class Environment(str, Enum):
    """
    Environment types
    """

    DEVELOPMENT = "development"
    PRODUCTION = "production"


class MailConfig(BaseSettings):
    """
    Email configurations
    """

    SUPPORT_EMAIL: str = "support@fastapi-boilertemplate.com"
    DEFAULT_EMAIL_FROM: str = "fastapi-boilertemplate <no-reply@fastapi-boilertemplate.com>"

    # SMTP Configs
    SMTP_HOST: str = Field(env="SMTP_HOST")
    SMTP_PORT: int = Field(env="SMTP_PORT")
    SMTP_USER: str = Field(env="SMTP_USER")
    SMTP_PASSWORD: str = Field(env="SMTP_PASSWORD")

    # Specify your template directory (Jinja2 templates)
    TEMPLATE_DIR: Path = Field(os.path.join(BASE_DIR, "templates"))


class PaystackConfig(BaseSettings):
    """
    Paystack configurations
    """

    PAYSTACK_SECRET_KEY: str = Field(..., env="PAYSTACK_SECRET_KEY")
    PAYSTACK_PUBLIC_KEY: str = Field(..., env="PAYSTACK_PUBLIC_KEY")
    PAYSTACK_BASE_URL: str = Field(default="https://api.paystack.co", env="PAYSTACK_BASE_URL")


class CloudinaryConfig(BaseSettings):
    """
    Cloudinary configurations
    """

    CLOUDINARY_CLOUD_NAME: str = Field(..., env="CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY: str = Field(..., env="CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: str = Field(..., env="CLOUDINARY_API_SECRET")


class GlobalConfig(BaseSettings):
    """
    Global configurations that are the same across all environments
    """

    APP_NAME: str = Field("Farm Riders Python Implementation", env="APP_NAME")
    APP_VERSION: str = Field("1.0", env="APP_VERSION")
    APPLICATION_CERTIFICATE: str = Field(default=CERTIFICATE)
    BASE_DIR: Path = Field(default=BASE_DIR)
    PORT: int = Field(8000, env="PORT")

    # Security / Auth Configs
    BCRYPT_SALT: int = 10
    ACCESS_TOKEN_JWT_EXPIRES_IN: str = Field("1h", env="ACCESS_TOKEN_JWT_EXPIRES_IN")
    REFRESH_TOKEN_JWT_EXPIRES_IN: str = Field("30d", env="REFRESH_TOKEN_JWT_EXPIRES_IN")
    DEFAULT_DB_TOKEN_EXPIRY_DURATION: str = Field("5m", env="DEFAULT_DB_TOKEN_EXPIRY_DURATION")

    # Email / Auth Configs
    SUPPORT_EMAIL: str = "support@FarmRiders.com"
    DEFAULT_EMAIL_FROM: str = "FarmRiders <no-reply@fastapi-boilertemplate.com>"
    USE_AWS_SES: bool = False

    MAILER: MailConfig = Field(default_factory=MailConfig)


class DevelopmentConfig(GlobalConfig):
    """
    Development configurations
    """

    DEBUG: bool = True
    JWT_SECRET: str
    MONGODB_URI: str = Field("mongodb://localhost:27017/FarmRiders")
    BASE_URL: str = "http://localhost:3000"

    PAYSTACK: PaystackConfig = Field(default_factory=PaystackConfig)

    CLOUDINARY: CloudinaryConfig = Field(default_factory=CloudinaryConfig)


class ProductionConfig(GlobalConfig):
    """
    Production configurations
    """

    DEBUG: bool = False
    JWT_SECRET: str
    MONGODB_URI: str
    BASE_URL: str
    PAYSTACK: PaystackConfig = Field(default_factory=PaystackConfig)
    CLOUDINARY: CloudinaryConfig = Field(default_factory=CloudinaryConfig)


def getenv():

    if DEPLOYMENT_ENV is None or DEPLOYMENT_ENV not in ["development", "production"]:
        raise ValueError("Invalid deployment environment")

    if DEPLOYMENT_ENV == "development":
        return DevelopmentConfig()

    return ProductionConfig()


settings = getenv()


print(settings.MONGODB_URI)
