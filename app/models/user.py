from mongoengine import Document, StringField, EmailField, BooleanField, FloatField, EnumField
from ..enums.user import UserRoles


class User(Document):

    firstname = StringField(required=True, min_length=3, max_length=50)

    lastname = StringField(required=True, min_length=3, max_length=50)

    password = StringField(required=True)

    email = EmailField(required=True, unique=True)

    is_verified = BooleanField(default=False)

    phone_number = StringField(required=True, unique=True)

    balance = FloatField(default=0.0)

    role = EnumField(UserRoles, required=True)

    meta = {"collection": "user", "strict": False}
