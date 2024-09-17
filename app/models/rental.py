from mongoengine import Document, StringField, DecimalField, URLField, ReferenceField, DateTimeField, EnumField
from ..enums.rental import RentalRequestStatus

from datetime import datetime


class Rentals(Document):
    name = StringField()
    price = DecimalField(precision=2)
    image_url = URLField()


class RentalRequest(Document):
    rental = ReferenceField(Rentals, required=True)
    total_price = DecimalField(precision=2)
    status = EnumField(RentalRequestStatus, default=RentalRequestStatus.pending)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
