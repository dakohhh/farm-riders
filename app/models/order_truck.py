from mongoengine import (
    Document,
    StringField,
    EnumField,
    ReferenceField,
    DateTimeField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    DecimalField,
    IntField,
    BooleanField,
)
from ..enums.ride import RideRequestStatus
from .user import User


class Location(EmbeddedDocument):
    address = StringField(required=True)
    latitude = DecimalField(required=True, precision=8)
    longitude = DecimalField(required=True, precision=8)


class OrderTruckRequest(Document):
    # Farmer or aggregator
    user = ReferenceField(User, required=True)
    driver = ReferenceField(User, required=True)
    pickup_location: Location = EmbeddedDocumentField(Location, required=True)
    dropoff_location: Location = EmbeddedDocumentField(Location, required=True)
    pickup_time = DateTimeField(required=True)
    status = EnumField(RideRequestStatus, default=RideRequestStatus.pending)
    special_instructions = StringField(required=False)

    type_of_goods = StringField(required=True)
    weight_of_goods = DecimalField(precision=2)
    quantity_of_goods = IntField()

    issued_insurance = BooleanField(default=False)
    insurance_partner = ReferenceField(User, default=None)

    insurance_cost = DecimalField(precision=2)

    total_cost = DecimalField(precision=2)

    # rental_duration_days = IntField()

    # special_instructions: Optional[str] = None
