from geopy.distance import geodesic
from ..libraries.socket import Location, Connection, socket_database, SocketMemoryDatabase



def calculate_distance(location1: Location, location2: Location):
    """
    Calculate distance between two points (latitude, longitude)
    using geopy's geodesic method.
    """
    coords_1 = (location1.latitude, location1.longitude)
    coords_2 = (location2.latitude, location2.longitude)
    return geodesic(coords_1, coords_2).kilometers




def find_nearest_drivers(pickup_location: Location, socket_database: SocketMemoryDatabase,  max_distance_km: float = 10.0):
    """
    Find drivers within max_distance_km of the pickup location.
    :param pickup_location: dictionary with 'latitude' and 'longitude'
    :param max_distance_km: maximum distance in kilometers
    """
    nearby_drivers = []

    
    # Iterate through all connected drivers in the in-memory database
    for sid, connection in socket_database.connections.items():

        if connection.user.role.value == "driver":

            driver_location = connection.location

            print(driver_location)

            # Calculate the distance between the pickup location and the driver's location

            distance = calculate_distance(pickup_location, driver_location)

            print(distance)

            if distance <= max_distance_km:

                nearby_drivers.append((connection, distance))

    # Sort drivers by distance

    nearby_drivers.sort(key=lambda x: x[1])
    
    return nearby_drivers
    
    
