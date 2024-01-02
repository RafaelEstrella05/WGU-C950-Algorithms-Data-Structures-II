


import csv
from Model.Package import Package
from Model.Dispatcher import Dispatcher


def load_package_data(dispatcher):
    # Open the CSV file
    with open('./Data/packages.csv', 'r') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)

        # Skip the header row
        next(reader)

        # Iterate through the rows
        for row in reader:
            package_id = row[0]
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            delivery_deadline = row[5]
            weight_kilo = row[6]
            special_notes = row[7]

            #print package information
            print("Package ID: ", package_id)
            print("Address: ", address)
            print("City: ", city)
            print("State: ", state)
            print("Zip Code: ", zip_code)
            print("Delivery Deadline: ", delivery_deadline)
            print("Weight: ", weight_kilo)
            print("Special Notes: ", special_notes)
            print()

            # Create a Package object and add it to the packages list
            package = Package(package_id, address, city, state, zip_code, delivery_deadline, weight_kilo, special_notes)

            # Add the package to the dispatcher
            dispatcher.load_package(package);

def load_distance_data(dispatcher):
    #load distances.csv into dispatcher
    with open('./Data/distances.csv', 'r') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)

        # Skip the header row
        next(reader)

        print("Loading distances into dispatcher...");

        distances = [];

        for row in reader:
            distances.append(row);
        
        #for each row in distances
        for i in range(len(distances)):
            location = distances[i][0].strip().replace('\n', ' ')
            num_destinations = len(distances[i]) - 1

            for j in range(num_destinations):
                destination = distances[j][0].strip().replace('\n', ' ')  # assuming that the distances are symmetrically stored
                distance = distances[i][j + 1].strip().replace('\n', '')

                #if distance is blank, swap location and destination
                if distance == "":      
                    distance = distances[j][i + 1] 

                    try:
                        # Convert distance to float
                        distance = float(distance)
                    except ValueError:
                        # If distance cannot be converted to float, set it to the value from distances[j][i + 1]
                        distance = distances[j][i + 1]

                    # Load graph node to dispatcher
                    dispatcher.load_graph_node(location, destination, distance)


print("Starting Script...");

#create dispatcher object
dispatcher = Dispatcher()

#load package data
load_package_data(dispatcher)

#load distance data
load_distance_data(dispatcher)

print("Distance data...");
dispatcher.print_distance_graph()

print("Package data...");
dispatcher.print_info();
