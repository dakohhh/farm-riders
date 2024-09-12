from mongoengine import (
    Document,
    StringField,
    EnumField,
    ReferenceField,
    URLField,
    BooleanField,
    EmbeddedDocument,
    IntField,
    EmbeddedDocumentField,
)
from .user import User
from ..enums.user import UserGender


class VehicleInfo(EmbeddedDocument):
    plate_number = StringField(required=True, max_length=20)
    vehicle_year = IntField(required=True)
    manufacturer_model = StringField(required=True, max_length=50)
    vehicle_color = StringField(required=True, max_length=20)
    proof_of_ownership = URLField()  # Proof of vehicle ownership


class Documents(EmbeddedDocument):
    selfie_photo = URLField(required=True)
    nin_photo = URLField()
    drivers_license_phone = URLField()


# https://example.com/verification_document.jpg


class Profile(Document):
    user = ReferenceField(User, required=True)

    firstname = StringField(min_length=3, max_length=50)

    lastname = StringField(min_length=3, max_length=50)

    gender = EnumField(UserGender)

    # NIN and Documents Upload for Verification
    nin = StringField(max_length=11)  # National ID number
    drivers_license_number = StringField(max_length=20)  # Driver's License number

    # Document Uploads
    documents = EmbeddedDocumentField(Documents, )

    meta = {'allow_inheritance': True, 'strict': False}


class DriverProfile(Profile):

    vehicle_info = EmbeddedDocumentField(VehicleInfo, default=None)

    has_vehicle = BooleanField(default=False)  # "I have a vehicle/truck"

    not_driving_self = BooleanField(default=False)  # "I have a vehicle/truck but not the one driving"

    available = BooleanField(default=False)
