from __future__ import annotations
from locations import create_example_countries_and_cities, City
from trip import Trip, create_example_trips
from vehicles import create_example_vehicles, Vehicle, CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley
from path_finding import find_shortest_path
from city_country_csv_reader import create_cities_countries_from_CSV
from map_plotting import plot_trip
import time
import math


def main():
    create_cities_countries_from_CSV("worldcities_truncated.csv")
    print("🍩🎂🍰🍞🥖🫓 Welcome to Papa Pierre's Pâtisseries 🍩🎂🍰🍞🥖🫓")
    print("Delivering our French yumminess to your doorstep💨💨💨")
    time.sleep(2)
    print("First, please create your vechicle ᕙ(`▿´)ᕗ")
    global fleet_of_vehicles
    fleet_of_vehicles = []  # to store vehicles created by user
    global trips_created
    trips_created = []  # to store trips created by user
    create_vehicle()  # let user create a vehicles list
    trip, trip_duration, vehicle = create_trip()  # three things which return from the create_trip() function
    plot_trip(trip)  # plot the trip created by user
    print("The trip {} will take {} hours with {}".format(trip, trip_duration, vehicle))
    time.sleep(1.5)
    progress(trip, vehicle)  # progress bar of the trip be printed out.


def int_input(prompt="", restricted_to=None):
    """
    Helper function that modifies the regular input method,
    and keeps asking for input until a valid one is entered. Input
    can also be restricted to a set of integers.

    Arguments:
      - prompt: String representing the message to display for input
      - restricted_to: List of integers for when the input must be restricted
                       to a certain set of numbers

    Returns the input in integer type.
    """
    while True:
        player_input = input(prompt)
        try:
            int_player_input = int(player_input)  # check whether input is integer
        except ValueError:
            print("Invalid input")  # if not integer, it will raise an error and let user input again
            continue
        if restricted_to is None:  # input is not restricted
            break
        elif int_player_input in restricted_to:  # input must be one of the elements of the list restricted_to
            break
        print("Invalid input")  # if input is not one of the elements of the list restricted_to, an error message will be printed out and user need to input again until a valid input is gained
    return int_player_input


def city_input(prompt=""):
    """
    Helper function that modifies the regular input method,
    and keeps asking for input until a existing city is entered.

    Arguments:
      - prompt: String representing the message to display for input

    Returns a valid City instance.
    """
    while True:
        player_input = input(prompt)
        for x in list(City.cities.values()):  # For loop to check whether city inputted by user is one of the cities in the file worldcities_truncated.csv
            if player_input.lower() == x.name.lower():
                return x
        print("Invalid city")


def create_vehicle():
    """
    create_vehicle is a function that enables user to create vehicles. Prior to creating a vehicles, 4 options will be given to user to choose from.
    If user selects option 1, user will need to create a vehicle from CrappyCrepeCar or DiplomacyDonutDinghy or TeleportingTarteTrolley with different speed.
    If user selects option 2, user will need to choose one of the vehicles from CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley with specified speed given.
    After creating a vehicle or choosing a vehicle from default, vehicles created by user will be appended to fleet_of_vehicles list.
    Then, user will jump back to select 1 of the 4 options again.
    If user selects option 3, user will jump to next function, create_trip if user has created at least a vehicle, if not user cannot proceed to create_trip function.
    If user selects option 4, a guideline will be printed out to user.
    """
    while True:
        time.sleep(1)
        print("\nYour current fleet:\n" + '\n'.join([str(x) for x in fleet_of_vehicles]))  # show the fleet_of_vehicles list to user
        time.sleep(1)
        option = int_input("\nPlease choose an option\n1. Create new vehicle\n2. Choose from default\n3. Continue to create trip\n4. User guide\n",[1, 2, 3, 4])  # Let the user to choose the action they want to perform
        print("_________________________________________________________________________________________")
        if option == 1:  # Create a new vehicle according to the existing classes
            print("\nWhich vehicle would you like to create?")
            option = int_input("1. CrappyCrepeCar\n2. DiplomacyDonutDinghy\n3. TeleportingTarteTrolley\n", [1, 2, 3])
            print("_________________________________________________________________________________________")
            if option == 1:  # The user create CrappyCrepeCar
                speed = int_input("\nWhat's the speed(km/h) of your CrappyCrepeCar?\n")  # input an integer for the speed of CrappyCrepeCar
                fleet_of_vehicles.append(CrappyCrepeCar(speed))  # build the vehicle as well as append it to list fleet_of_vehicles

            elif option == 2:  # The user create DiplomacyDonutDinghy
                in_country_speed = int_input("\nWhat's the speed(km/h) for two cities in the same country of your DiplomacyDonutDinghy?\n")  # input an integer for the in_country_speed of DiplomacyDonutDinghy
                between_primary_speed = int_input("\nWhat's the speed(km/h) between two primary cities for your DiplomacyDonutDinghy?\n")  # input an integer for the between_primary_speed of DiplomacyDonutDinghy
                fleet_of_vehicles.append(DiplomacyDonutDinghy(in_country_speed,between_primary_speed))  # build the vehicle as well as append it to list fleet_of_vehicles

            else:  # The user create TeleportingTarteTrolley
                travel_time = int_input("\nHow long will your TeleportingTarteTrolley travels in fixed time between two cities within the maximum distance?\n")  # input an integer for the travel_time of TeleportingTarteTrolley
                max_distance = int_input("\nWhat's the maximum distance(km) that your TeleportingTarteTrolley can travel?\n")  # input an integer for the max_distance of TeleportingTarteTrolley
                fleet_of_vehicles.append(TeleportingTarteTrolley(travel_time, max_distance))  # append to list fleet_of_vehicles

        elif option == 2:
            example_vehicles = create_example_vehicles()  # a list of CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley with default speed parameter will be stored under example_vehicles variable
            for i in range(len(example_vehicles)):
                print(str(i + 1) + ". " + str(example_vehicles[i]))
            selected_vehicles = int_input("\nFrom those example vehicles, which vehicle would you like to choose?\n",[1, 2, 3])  # let user choose 1 of the vehicles out of the 3 choices given
            print("_________________________________________________________________________________________")
            if selected_vehicles == 1:
                fleet_of_vehicles.append(example_vehicles[0])  # append to list fleet_of_vehicles
            elif selected_vehicles == 2:
                fleet_of_vehicles.append(example_vehicles[1])  # append to list fleet_of_vehicles
            else:
                fleet_of_vehicles.append(example_vehicles[2])  # append to list fleet_of_vehicles

        elif option == 3:
            if len(fleet_of_vehicles) == 0:  # to ensure at least a vehicle is in the list fleet_of_vehicles
                print("You didn't have a vehicle to use!! \n ")
            else:
                break  # break the while loop and jump to the next function

        elif option == 4:
            print("""
You can create your own vehicle!!!
There are 3 vehicles you can chooose from:
CrappyCrepeCar:          A flying car that can travel between any two cities in the world, but moves pretty 
                         slowly.

DiplomacyDonutDinghy:    A small boat which is licensed to travel on diplomatic hyperlanes. So it moves extra 
                         fast between capital cities. It can also travel between any two cities in the same 
                         country.However, it can only move from one country to another via their capitals.

TeleportingTarteTrolley: A trolley bus that can teleport between any two cities if they are close enough, 
                         regardless of countries. Because teleportation technology is still in its infancy,
                         it takes time to program and execute a blink between two cities.

If you're lazy to create your own vehicle, feel free to choose from our current vehicle! 
PS: You are advised to create at least 1 vehicle for each type of vehicle to smoothen your tour XD""")
            input("Press enter to continue")


def create_trip():
    """
    create_trip is a function which enables user to create a trip desired. Prior to creating a trip, 4 options will be given to user to choose from.
    If user chooses option 1, user will need to choose 1 location out of the 4 default locations printed out with for loop.
    If user chooses option 2, user will need to add city manually.
    A while loop will be used to ensure user to add at least 2 different cities and no cities are added consecutively so there is a valid path.
    If user chooses option 3, user will need to input departure location and arrival location.
    Then, the trip created will be added to a list named trip_created
    When user chooses option 4, list trip_created will be shown to them using a for loop.
    They can choose 1 of the trips.
    After choosing a trip, user can either use the default vehicle given(fastest vehicle to complete the trip) or choose a vehicle from list fleet_of_vehicles.
    If the vehicle chose is invalid(duration = math.inf), user need to select another vehicle until a valid vehicle is selected
    Having selected a valid vehicle, the simulation of the trip will be printed out using progress() function.

    Returns trip,duration,vehicle
    """
    city_list = list(City.cities.values())
    example_trips = create_example_trips()  # a list of default trips will be stored under example_trips variable
    while True:
        time.sleep(1)
        print("\nYour current trip:\n" + '\n'.join([str(x) for x in trips_created]))  # show the fleet_of_vehicles list to user
        time.sleep(1)
        option = int_input("\nPlease choose an option\n1. Choose from default \n2. Manually adding city\n3. Use path finding system\n4. Start onboard navigation🚗ψ(｀∇´)ψ\n",[1, 2, 3, 4])
        print("_________________________________________________________________________________________")
        if option == 1:
            for i in range(len(example_trips)):  # for loop to print out 4 default trips
                print(str(i + 1) + ". " + str(example_trips[i]))
            selected_trips = int_input("From those example trips, which trip would you like to choose?\n",list(range(1, len(example_trips) + 1)))
            print("_________________________________________________________________________________________")
            trips_created.append(example_trips[selected_trips - 1])  # trip chosen by user
        elif option == 2:
            path = []  # store the cities added by user
            previous_city = None  # used to compare with the most recent city added to ensure no same citied addded consecutively
            while True:
                city = city_input("\nWhich city would you like to add?\n")  # user input a city
                if city == previous_city:  # if same cities addded, user need to input a new city again.
                    print("Cannot travel same cities consecutively")
                    continue
                previous_city = city
                path.append(city)  # append the newly added city
                option = int_input("\nDo you like to add another city?\n1. Yes\n2. No\n", [1, 2])
                if option == 1:  # continue to add city
                    continue
                else:
                    if len(path) < 2:  # user need to add at least 2 cities
                        print("You must add at least 2 cities")
                        continue
                    trip = Trip(path[0])
                    for city in path[1:]:  # create a trip with add_next_city function
                        trip.add_next_city(city)
                    break
            trips_created.append(trip)
        elif option == 3:
            dep = city_input("Where do you want to start from?\n")  # user input departure location
            des = city_input("Where do you want to go?\n")  # user input arrival location
            trips = []  # list to store trip of each valid vehicle of fleet_of_vehicles list
            i = 1
            for v in fleet_of_vehicles:
                trip = find_shortest_path(v, dep, des)
                trips.append(trip)
                print(str(i) + ". {}: {}".format(v, trip))
                i += 1
            if all(i is None for i in trips):  # If there is no valid vehicle, user will jump back to create_vehicle function
                print("Vehicle list created does not have a vehicle which can be used to deliver from selected location")
                option = int_input("Do you wish to recreate vehicles or choose another path?\n1. Recreate vehicle\n2. Choose another path\n",[1, 2])
                print("_________________________________________________________________________________________")
                if option == 1:
                    print("Jumping back to create vehicle🚗🚗🚗💨💨💨")
                    create_vehicle()  # Jump back to create vehicle if user choose to recrete vehicle
                    continue
                else:
                    continue
            option = int_input("Which path do you wish to add?\n", list(range(1, len(fleet_of_vehicles) + 1)))
            trips_created.append(trips[option - 1])
        else:
            if len(trips_created) == 0:
                print("Please create a trip before starting onboard navigation !!!")
                time.sleep(1)
                continue
            else:
                break

    # For loop to print current trips
    for i in trips_created:
        print(str(trips_created.index(i) + 1) + ". " + str(i))
    selection = int_input("From trip above, which one you would like to choose?\n",list(range(1, len(trips_created) + 1)))
    print("_________________________________________________________________________________________")
    trip = trips_created[selection - 1]
    while True:
        vehicle, duration = trip.find_fastest_vehicle(fleet_of_vehicles)
        if vehicle == None:
            print("There is no vehicle that can complete your trip, please create another vehicle")
            create_vehicle()
        else:
            break
    print("The fastest vehicle for your trip is " + vehicle.__str__() + ", and it takes " + str(duration) + " hours to travel.")

    option = int_input("Do you wish to use this vehicle?\n1. Yes\n2. No\n", [1, 2])
    if option == 2:
        for i in fleet_of_vehicles:
            print(str(fleet_of_vehicles.index(i) + 1) + ". " + str(i) + " : " + str(trip.total_travel_time(i)) + " hours")
        while True:
            selection = int_input("From vehicle above, which one you would like to choose?(The vehicle with None hours is restricted)\n",list(range(1, len(fleet_of_vehicles) + 1)))
            print("_________________________________________________________________________________________")
            vehicle = fleet_of_vehicles[selection - 1]  # vehicle is chosen from the list
            duration = trip.total_travel_time(vehicle)
            if duration != math.inf:
                break
            else:
                print("Please choose another valid vehicle, chosen vehicle cannot complete the trip")
                continue
    return trip, duration, vehicle


def progress(trip: Trip, vehicle: Vehicle):
    """
    progress function is used to print out the progress bar and cities involved in the current leg.
    Arguements:
                trip : a trip that has been chosen
                vehicle : a vehicle that has been chosen to travel
    """
    progress_bar_size = 100
    download_speed = 0.1
    for i in range(len(trip.destination) - 1):
        times = vehicle.compute_travel_time(trip.destination[i], trip.destination[i + 1])  # to be used to show 2 different cities in the progress bar
        download_time = times * download_speed  # total time needed to print out the whole progress bar
        execution_time = download_time / progress_bar_size  # time interval to update the progress bar
        print("\nTravelling to " + str(trip.destination[i + 1]))  # display cities that invoked in the current list
        print(str(trip.destination[i]) + " " * 52 + str(trip.destination[i + 1]),end='\r')  # to ensure the destination location remain same place when progress bar processing
        for x in range(101):
            time.sleep(execution_time)
            print(str(trip.destination[i]) + " " + '✿' * ((x + 1) // 2) + " ", end='\r')
    print("\nYour order has been delivered. Thanks for supporting us!(>‿◠)✌")


if __name__ == "__main__":
    main()