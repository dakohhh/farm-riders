from mongoengine import Document, StringField, ReferenceField, URLField
from .user import User


class Profile(Document):

    nin = StringField(max_length=11, min_length=11, default=None)

    verification_document = URLField(default=None)

    user: User = ReferenceField(User, required=True)
