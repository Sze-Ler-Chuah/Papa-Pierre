import city_country_csv_reader
from locations import City, Country
from trip import Trip
from vehicles import Vehicle, create_example_vehicles, CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley
import networkx as nx
import matplotlib.pyplot as plt
import math


def find_shortest_path(vehicle: Vehicle, from_city: City, to_city: City) -> Trip:
    """
    Returns a shortest path between two cities for a given vehicle,
    or None if there is no path.
    """
    # cases for CrappyCrepeCar which can travel directly between cities without restriction
    if type(vehicle) == CrappyCrepeCar:
        x = Trip(from_city)  # create Trip instance
        x.add_next_city(to_city)
        return x  # return path from departure to destination as Trip
    # cases for DiplomacyDonutDinghy and TeleportingTarteTrolley which have some restriction
    else:
        G = nx.Graph()  # create a graph in networkx
        keys_list = list(City.cities.keys())  # a list stored cities id
        # to ensure all cities are computed with the rest
        for x in range(len(City.cities) - 1):  # iterate through all cities except the last city
            for y in range(x + 1, len(City.cities)):  # iterate through cities after x
                # store city id which is used to access dictionary cities
                a = keys_list[x]
                b = keys_list[y]
                # only connect cites that are reachable for corresponding vehicles
                if vehicle.compute_travel_time(City.cities[a], City.cities[b]) != math.inf:
                    # connect two cities by using city objects as the nodes and its travel time as the edge weights
                    G.add_edge(City.cities[a], City.cities[b], weight_=vehicle.compute_travel_time(City.cities[a], City.cities[b]))

        try:
            # try to find the shortest path from depature to destination
            path = nx.shortest_path(G, source=from_city, target=to_city)  # return a list of cities in a shortest path from the source to the target and store to path
            # create Trip according the path list
            x = Trip(from_city)
            for y in path[1:]:
                x.add_next_city(y)
            return x  # return shortest path that is found from departure to destination as Trip
        except:
            # raise an error when no path is found and return None
            return None


if __name__ == "__main__":
    city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")

    vehicles = create_example_vehicles()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    for vehicle in vehicles:
        print("The shortest path for {} from {} to {} is {}".format(vehicle, melbourne, tokyo, find_shortest_path(vehicle, melbourne, tokyo)))