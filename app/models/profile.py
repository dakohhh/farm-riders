from mongoengine import Document, StringField, ReferenceField, URLField
from .user import User


class Profile(Document):

    nin = StringField(max_length=11, min_length=11, required=True)

    verification_document = URLField(required=True)

    user: User = ReferenceField(User)
