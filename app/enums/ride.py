from enum import Enum


class RideRequestStatus(Enum):
    pending = "pending"
    assigned = "assigned"
    completed = "completed"
    cancelled = "cancelled"