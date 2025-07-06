from vehicles import Vehicle, CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley
from vehicles import create_example_vehicles
from locations import City, Country
from locations import create_example_countries_and_cities
import math


class Trip():
    """
    Represents a sequence of cities.
    """

    def __init__(self, departure: City) -> None:
        """
        Initialises a Trip with a departure city.
        """
        self.departure = departure  # Stores value of departure location
        self.destination = [departure]  # A list that stores all the cities in the path

    def add_next_city(self, city: City) -> None:
        """
        Adds the next city to this trip.
        """
        self.destination.append(city)  # Append next city in the list destination

    def total_travel_time(self, vehicle: Vehicle) -> float:
        """
        Returns a travel duration for the entire trip for a given vehicle.
        Returns math.inf if any leg (i.e. part) of the trip is not possible.
        """
        total_t = 0
        for city in range(len(self.destination) - 1):
            t = vehicle.compute_travel_time(self.destination[city], self.destination[
                city + 1])  # Let t be the time of a city to next city for a given vehicle
            if t is math.inf:
                return t  # Return vehicle compute travel time if it is math.inf
            total_t += t  # Add vehicle compute travel time to total time
        return total_t  # Return total time of entire Trip

    def find_fastest_vehicle(self, vehicles: list[Vehicle]) -> (Vehicle, float):

        """
        Returns the Vehicle for which this trip is fastest, and the duration of the trip.
        If there is a tie, return the first vehicle in the list.
        If the trip is not possible for any of the vehicle, return (None, math.inf).
        """
        shortest_duration = math.inf  # Assume that the shortest duration of trip is math.inf
        fastest_vehicle = ''
        for vehicle in vehicles:  # Loop the vehicle in the vehicles list
            t = self.total_travel_time(vehicle)
            if t < shortest_duration:  # A situation of total travel time of that vehicle < shortest duration of trip
                shortest_duration = t  # The shortest_duration is the total travel time of that vehicle now
                fastest_vehicle = vehicle  # The fastest vehicle is that vehicle now
        if shortest_duration == math.inf:
            return (None, math.inf)
        return (fastest_vehicle, shortest_duration)  # Return a tuple in the form of(fastest_vehicle,shortest_duration)

    def __str__(self) -> str:
        """
        Returns a representation of the trip as a sequence of cities:
        City1 -> City2 -> City3 -> ... -> CityX
        """
        string = ""
        for city in self.destination:
            string += f'{city} -> '
        return string.strip(' ->')  # Return a string that has removed ' ->' after last city


def create_example_trips() -> list[Trip]:
    """
    Creates examples of trips.
    """
    # first we create the cities and countries
    create_example_countries_and_cities()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    sydney = australia.get_city("Sydney")
    canberra = australia.get_city("Canberra")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")
    US = Country.countries["United States"]
    NY = US.get_city("New York")

    # then we create trips
    trips = []
    for cities in [(melbourne, sydney), (canberra, tokyo), (melbourne, canberra, tokyo), (canberra, melbourne, tokyo),(melbourne, canberra, NY)]:
        trip = Trip(cities[0])
        for city in cities[1:]:
            trip.add_next_city(city)
        trips.append(trip)
    return trips


if __name__ == "__main__":
    vehicles = create_example_vehicles()
    trips = create_example_trips()

    for trip in trips:
        vehicle, duration = trip.find_fastest_vehicle(vehicles)
        print("The trip {} will take {} hours with {}".format(trip, duration, vehicle))