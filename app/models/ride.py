from mongoengine import Document, StringField, EnumField, ReferenceField, DateTimeField, Decimal128Field, EmbeddedDocument, EmbeddedDocumentField, DecimalField
from ..enums.ride import RideRequestStatus
from .user import User

DecimalField()
class Location(EmbeddedDocument):
    address = StringField(required=True)
    latitude = DecimalField(required=True, precision=8)
    longitude = DecimalField(required=True, precision=8)



class RideRequest(Document):
    # Farmer or aggregator
    user = ReferenceField(User, required=True)
    driver = ReferenceField(User, default=None)
    pickup_location = EmbeddedDocumentField(Location, required=True)
    dropoff_location = EmbeddedDocumentField(Location, required=True)
    pickup_time = DateTimeField(required=True)
    status = EnumField(RideRequestStatus, default=RideRequestStatus.pending)
    special_instructions = StringField(required=False)