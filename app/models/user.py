from mongoengine import Document, StringField, EmailField, BooleanField, FloatField, EnumField
from ..enums.user import UserRoles


class User(Document):

    password = StringField(required=True)

    email = EmailField(required=True, unique=True)

    is_verified = BooleanField(default=False)

    has_completed_profile = BooleanField(required=True, default=False)

    phone_number = StringField(required=True, unique=True)

    balance = FloatField(default=0.0)

    role = EnumField(UserRoles, required=True)

    meta = {"collection": "user", "strict": False}
