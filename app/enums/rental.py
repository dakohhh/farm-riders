from enum import Enum


class RentalRequestStatus(Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
