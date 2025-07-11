from __future__ import annotations
from enum import Enum
from geopy.distance import great_circle
import math


class CapitalType(Enum):
    """
    The different types of capitals (e.g. "primary").
    """
    primary = "primary"
    admin = "admin"
    minor = "minor"
    unspecified = ""

    def __str__(self) -> str:
        return self.value


class Country():
    """
    Represents a country.
    """
    countries = dict()  # A dict that associates country names to instances.

    def __init__(self, name: str, iso3: str) -> None:
        """
        Creates an instance with a country name and a country ISO code with 3 characters.
        """
        self.name = name
        self.iso3 = iso3
        Country.countries[name] = self  # Add country instance to the dictionary based on its names
        self.cities = []  # A list to store all cities for particular country

    def _add_city(self, city: City):
        """
        Adds a city to the country.
        """
        self.cities.append(city)  # To add city into a list which called cities

    def get_cities(self, capital_types: list[CapitalType] = None) -> list[City]:
        """
        Returns a list of cities of this country.

        The argument capital_types can be given to specify a subset of the capital types that must be returned.
        Cities that do not correspond to these capital types are not returned.
        If no argument is given, all cities are returned.
        """
        if capital_types == None:
            return self.cities  # Return a list that stores all cities if no argument is given
        else:
            cities_ret = []  # A list that stores city needed
            for city in self.cities:  # Loop in the list of cities
                if city.capital_type in capital_types:  # Check the capital type of city is in the list of capital_types or not
                    cities_ret.append(city)  # Append city into list cities_ret
            if len(cities_ret) == 0:  # A situation of list cities_ret is empty
                return None
            return cities_ret  # If list cities_ret is not empty,return all cities

    def get_city(self, city_name: str) -> City:
        """
        Returns a city of the given name in this country.
        Returns None if there is no city by this name.
        If there are multiple cities of the same name, returns an arbitrary one.
        """
        for city in self.cities:
            if city.name == city_name:  # Check city name in list cities is equal to the given city's name or not
                return city  # Return arbitrary city name
        return None  # If there is no city same by this name,return None

    def __str__(self) -> str:
        """
        Returns the name of the country.
        """
        return self.name

class City():
    """
    Represents a city.
    """

    cities = dict()  # A dict that associates city IDs to instances.

    def __init__(self, name: str, latitude: str, longitude: str, country: str, capital_type: str, city_id: str) -> None:
        """
        Initialises a city with the given data.
        """
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.country = Country.countries[country]
        self.capital_type = CapitalType(capital_type)
        self.city_id = city_id
        City.cities[city_id] = self
        self.country._add_city(self)

    def distance(self, other_city: City) -> int:
        """
        Returns the distance in kilometers between two cities using the great circle method,
        rounded up to an integer.
        """
        city_1 = (self.latitude, self.longitude)  # A tuple of depature in the form of (lon,lat) in decimal degrees
        city_2 = (other_city.latitude, other_city.longitude)  # A tuple of destination in the form of (lon,lat) in decimal degrees
        return math.ceil(great_circle(city_1, city_2).kilometers)  # Return distance of two cities using the great circle method,rounded up to an integer by math.ceil method

    def __str__(self) -> str:
        """
        Returns the name of the city and the country ISO3 code in parentheses.
        For example, "Melbourne (AUS)".
        """
        return (self.name + " (" + self.country.iso3 + ")")


def create_example_countries_and_cities() -> None:
    """
    Creates a few Countries and Cities for testing purposes.
    """
    australia = Country("Australia", "AUS")
    melbourne = City("Melbourne", "-37.8136", "144.9631", "Australia", "admin", "1036533631")
    canberra = City("Canberra", "-35.2931", "149.1269", "Australia", "primary", "1036142029")
    sydney = City("Sydney", "-33.865", "151.2094", "Australia", "admin", "1036074917")
    japan = Country("Japan", "JPN")
    tokyo = City("Tokyo", "35.6839", "139.7744", "Japan", "primary", "1392685764")


def test_example_countries_and_cities() -> None:
    """
    Assuming the correct cities and countries have been created, runs a small test.
    """
    australia = Country.countries['Australia']
    canberra = australia.get_city("Canberra")
    melbourne = australia.get_city("Melbourne")
    sydney = australia.get_city("Sydney")
    print("The distance between {} and {} is {}km".format(melbourne, sydney, round(melbourne.distance(sydney))))
    print(australia.get_cities([CapitalType.minor]))
    for city in australia.get_cities([CapitalType.admin, CapitalType.primary]):
        print("{} is a {} capital of {}".format(city, city.capital_type, city.country))


if __name__ == "__main__":
    create_example_countries_and_cities()
    test_example_countries_and_cities()
