
import csv
from Model.Package import Package
from Model.Dispatcher import Dispatcher
from Model.Truck import Truck

#load package data
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

            # Create a Package object and add it to the packages list
            package = Package(package_id, address, city, state, zip_code, delivery_deadline, weight_kilo, special_notes)

            # Add the package to the dispatcher
            dispatcher.load_package(package);



#load distance matrix
def load_distance_matrix(dispatcher):
    with open('./Data/distances.csv', 'r') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)

        # Skip the header row
        next(reader)

        print("Loading distances into dispatcher...")

        csv_data = []
        location_labels = [] #list of strings
        distance_matrix = []  # distance_matrix as list of lists

        row_index = 0
        for row in reader:
            location_name = row[0].strip().replace('\n', ' ')
            location_labels.append(location_name)

            distances = []  # for one row of distances
            # for the rest of the columns in the row, grab the distance and add to distances
            for k in range(1, len(row)):
                distance = row[k]
                distances.append(distance)

            csv_data.append(distances)
            row_index += 1

        # Convert csv_data to distance_matrix, from string to float
        for i in range(len(csv_data)):
            distances = []
            for j in range(len(csv_data[i])):
                distance = csv_data[i][j].strip()

                if distance == "":
                    distance = csv_data[j][i].strip()

                distance = float(distance)

                distances.append(distance)

            distance_matrix.append(distances)

        # load distance data into dispatcher
        dispatcher.load_distance_data(location_labels, distance_matrix)

        print("\n Location Labels:")
        
        #for every key in location_labels, print the key and the value
        for key in location_labels:
            print(key, ":", location_labels[key])

        print("\n Distance Matrix:")
        
        for i in range(len(distance_matrix)):
            print(distance_matrix[i])
