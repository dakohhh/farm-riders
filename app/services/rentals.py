from ..models.rental import Rentals
from ..schema.rentals import ListRentalsOut


class RentalService:
    @staticmethod
    async def get_all_rentals():
        query = Rentals.objects().as_pymongo()

        rentals = ListRentalsOut(rentals=query)

        return rentals
