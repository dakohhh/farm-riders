from enum import Enum


class UserRoles(Enum):
    admin = "admin"
    aggregator = "aggregator"
    driver = "driver"
    farmers = "farmers"


class UserGender(Enum):
    male = "male"
    female = "female"
    other = "other"
