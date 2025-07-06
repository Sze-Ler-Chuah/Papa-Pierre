from abc import ABC, abstractmethod
from locations import CapitalType, City, Country, create_example_countries_and_cities
import math


class Vehicle(ABC):
    """
    A Vehicle defined by a mode of transportation, which results in a specific duration.
    """

    @abstractmethod
    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        """
        pass


class CrappyCrepeCar(Vehicle):
    """
    A type of vehicle that:
        - Can go from any city to any other at a given speed.
    """

    def __init__(self, speed: int) -> None:
        """
        Creates a CrappyCrepeCar with a given speed in km/h.
        """
        self.speed = speed

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        """
        return math.ceil(departure.distance(arrival) / self.speed)  # Return travel duration of trip (distance between depature and arrival /speed of CrappyCrepeCar),and rounded up by math.ceil method

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "CrappyCrepeCar (100 km/h)"
        """
        return ("CrappyCrepeCar (" + str(self.speed) + " km/h)")


class DiplomacyDonutDinghy(Vehicle):
    """
    A type of vehicle that:
        - Can travel between any two cities in the same country.
        - Can travel between two cities in different countries only if they are both "primary" capitals.
        - Has different speed for the two cases.
    """

    def __init__(self, in_country_speed: int, between_primary_speed: int) -> None:
        """
        Creates a DiplomacyDonutDinghy with two given speeds in km/h:
            - one speed for two cities in the same country.
            - one speed between two primary cities.
        """
        self.in_country_speed = in_country_speed  # speed for two cities in the same country.
        self.between_primary_speed = between_primary_speed  # speed between two primary cities.

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.
        """
        if departure.country == arrival.country:  # A situation of depature city located country same as arrival city located country
            return math.ceil(departure.distance(arrival) / self.in_country_speed)  # return the travel duration of trip (distance between 2 cities / in_country_speed),and rounded up by math.ceil method
        elif departure.capital_type == CapitalType.primary and arrival.capital_type == CapitalType.primary:  # A situation of depature city and arrival city both capital_type are "primary"
            return math.ceil(departure.distance(arrival) / self.between_primary_speed)  # return the travel duration of trip (distance between 2 cities / between_primary_speed),and rounded up by math.ceil method
        else:  # Other situation except of 2 situation above
            return math.inf

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "DiplomacyDonutDinghy (100 km/h | 200 km/h)"
        """
        return ("DiplomacyDonutDinghy (" + str(self.in_country_speed) + " km/h | " + str(
            self.between_primary_speed) + " km/h)")


class TeleportingTarteTrolley(Vehicle):
    """
    A type of vehicle that:
        - Can travel between any two cities if the distance is less than a given maximum distance.
        - Travels in fixed time between two cities within the maximum distance.
    """

    def __init__(self, travel_time: int, max_distance: int) -> None:
        """
        Creates a TarteTruck with a distance limit in km.
        """
        self.travel_time = travel_time
        self.max_distance = max_distance

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.
        """
        if departure.distance(arrival) < self.max_distance:  # A situation of distance between depature and arrival <= the maximun distance
            return self.travel_time
        else:
            return math.inf

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "TeleportingTarteTrolley (5 h | 1000 km)"
        """
        return ("TeleportingTarteTrolley (" + str(self.travel_time) + " h | " + str(self.max_distance) + " km)")


def create_example_vehicles() -> list[Vehicle]:
    """
    Creates 3 examples of vehicles.
    """
    return [CrappyCrepeCar(200), DiplomacyDonutDinghy(100, 500), TeleportingTarteTrolley(3, 2000)]


if __name__ == "__main__":
    create_example_countries_and_cities()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    canberra = australia.get_city("Canberra")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    vehicles = create_example_vehicles()

    for vehicle in vehicles:
        for from_city, to_city in [(melbourne, canberra), (tokyo, canberra), (tokyo, melbourne)]:
            print("Travelling from {} to {} will take {} hours with {}".format(from_city, to_city, vehicle.compute_travel_time(from_city,to_city),vehicle))