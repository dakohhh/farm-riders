from ..models.vehicle import Vehicle
from ..schema.vehicle import VehicleOut, ListVehicleOut


class VehicleService:
    @staticmethod
    async def get_all_vehicles():
        query = Vehicle.objects().as_pymongo()

        vehicles = ListVehicleOut(vehicles=query)

        return vehicles
