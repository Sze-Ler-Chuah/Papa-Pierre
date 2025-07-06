import city_country_csv_reader
from locations import create_example_countries_and_cities
from trip import Trip, create_example_trips
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import math


def plot_trip(trip: Trip, projection='merc', line_width=2, colour='b') -> None:
    """
    Plots a trip on a map and writes it to a file.
    Ensures a size of at least 50 degrees in each direction.
    Ensures the cities are not on the edge of the map by padding by 5 degrees.
    The name of the file is map_city1_city2_city3_..._cityX.png.
    """

    name = "map_"  # The name of map
    m = Basemap()  # Use to find gcpoints for many purposes(details are at below)

    # store the longitude & latitude of all location
    lng_list = []
    lat_list = []

    center_lng = []  # store the longitude gcpoints to determine the center longitude(for robin projection)
    lat_range = []  # store the latitude gcpoints to determine the range of latitude(for merc/user selected projection)
    name_list = []  # store the name of each destination to put into the legend of the map

    # A nested list which is used to determine which plotting method(drawgreatcircle or m.plot with gcpoints) to prevent line being cut
    draw_lng = []
    draw_lat = []

    # To determine the extreme points of the map (for merc/user selected projection)
    lng_max = trip.departure.longitude  # maximum(upper right) longitude
    lng_min = trip.departure.longitude  # minimum(lower left) longitude
    lat_max = trip.departure.latitude  # maximum(upper right) latitude
    lat_min = trip.departure.latitude  # minimum(lower left) latitude
    exist_name = []  # To prevent duplicate name of location occur in legend
    for city in trip.destination:  # A for loop to add on some elements into the list or replace the original value (details are at below)
        name += f"{city}"[:-6] + "_"  # To add a string(the name of city) into the name

        # append the longitude,latitude and name of each city into corresponding list
        lng_list.append(city.longitude)
        lat_list.append(city.latitude)
        name_list.append(city.__str__())

        # To replace the value of the maximum(upper right) and minimum(lower left) of longitude and latitude based on the city's coordinate
        if city.longitude > lng_max:
            lng_max = city.longitude
        if city.longitude < lng_min:
            lng_min = city.longitude
        if city.latitude > lat_max:
            lat_max = city.latitude
        if city.latitude < lat_min:
            lat_min = city.latitude
    # If the route is long enough(using the range of longitude), we set the projection to robin to prevent the route being cut(as robin can set the center longitude)
    if lng_max - lng_min > 100:
        projection = 'robin'

        # A for loop use to find the gcpoints of the route(details are at below)
        for k in range(len(lng_list) - 1):
            a, b = m.gcpoints(lng_list[k], lat_list[k], lng_list[k + 1], lat_list[k + 1], 1000)  # compute 1000 points along a great circle for each depature and destination city.
            center_lng += a  # store the latitude of the points computed above to determine the center longitude
            # Append the gcpoints list of each route into the nested list
            draw_lng.append(a)
            draw_lat.append(b)

        center_lng = list(map(lambda x: int(x), center_lng))  # Make the longitude to be integer(for better calculation)
        # line 71 to 77 is to calculate the nearest center of the departure and final destination city(the calculation detail will not explain in detail as it is very hard TAT)
        if 0 in center_lng or (lng_max < 0 and lng_min < 0) or (lng_max > 0 and lng_min > 0):
            lng_center = (lng_max + lng_min) // 2
        else:
            if lng_max > abs(lng_min):
                lng_center = (lng_max + lng_min) // 2 - 180

            else:
                lng_center = (lng_max + lng_min) // 2 + 180

                # To set the center longitude of the robin projection map (as we find that positive longitude will result in inverted map, so we need to convert positive longitude into negative)
        if lng_center > 0:
            lng_center_m = lng_center - 360
        else:
            lng_center_m = lng_center

    # If the route isn't that long, it will use merc(default projection) or any projection that the user set
    else:
        # The for loop below is use to calculate the latitude range of the route(to prevent the map doesn't show the route completely)
        for k in range(len(lng_list) - 1):
            x, y = m.gcpoints(lng_list[k], lat_list[k], lng_list[k + 1], lat_list[k + 1], 1000)
            lat_range += y  # add the new range of latitude for each route into the old list
            # Append the gcpoints list of each route into the nested list
            draw_lng.append(x)
            draw_lat.append(y)

        # To determine the maximum and minimum latitude to set as the size of basemap
        lat_min = min(lat_range)
        lat_max = max(lat_range)
        lng_center_m = None  # This projection does not need center longitude as parameter

    fig = plt.figure(figsize=(10, 6))  # set the figure size of the map

    # Plot the map out with the parameter calculated above
    m = Basemap(lon_0=lng_center_m, llcrnrlon=lng_min - 3, llcrnrlat=lat_min - 3, urcrnrlon=lng_max + 3,urcrnrlat=lat_max + 3, projection=projection)
    # The for loop below is to plot the point of each location and also create the legend for the location name
    for l in range(len(lng_list)):
        if name_list[l] not in exist_name:  # To prevent duplicate point/legend element
            x, y = m(lng_list[l], lat_list[l])
            m.plot(x, y, 'o', alpha=0.8, markersize=10, label=name_list[l])  # Plot the point out
            exist_name.append(name_list[l])  # Use to store names of each location

    # The for loop below is to draw the line of each route
    for x in range(len(draw_lng)):
        # To find the corner longitude of robin projection
        if projection != "robin":
            sep = math.inf
        else:
            sep = int(lng_center + (-1) ** (int(lng_center > 0)) * 180)

        # The below if-else is to determine which plotting method to be used(specifically for robin projection)
        # If the route is found to cross the corner of the map(in robin), use drawgreatcircle to draw the line
        if sep in list(map(lambda z: int(z), draw_lng[x])) or sep + 1 in list(map(lambda z: int(z), draw_lng[x])):
            m.drawgreatcircle(trip.destination[x].longitude, trip.destination[x].latitude,trip.destination[x + 1].longitude, trip.destination[x + 1].latitude, linewidth=line_width,color=colour)
        # If not(also using merc projection), use gcpoints and plot the line (as gcpoints will not cut the line in half when the route is in high latitude)
        else:
            j, k = m.gcpoints(lng_list[x], lat_list[x], lng_list[x + 1], lat_list[x + 1], 300)
            m.plot(j, k, color=colour, linewidth=line_width)
            # add more details in the map to improve the appearance of it
    m.drawcoastlines()
    m.drawmapboundary(fill_color='lavender')
    m.fillcontinents(color='cornsilk', lake_color='lavender')
    plt.legend(loc='lower right', borderpad=1.5, fontsize=5)  # add the legend about the name of each points for better visualization
    plt.title(name.strip("_")[4:])  # saved as a map title city1_city2..cityX
    plt.savefig(name.strip("_"))  # saved as a file named map_city1_city2..cityX.png


if __name__ == "__main__":
    city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")
    create_example_countries_and_cities()
    trips = create_example_trips()

    for trip in trips:
        plot_trip(trip)