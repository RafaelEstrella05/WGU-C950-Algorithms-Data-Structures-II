


import csv
from Model.Package import Package
from Model.Dispatcher import Dispatcher



print("Starting Script...");

#create dispatcher object
dispatcher = Dispatcher()

# Open the CSV file
with open('./Data/distances.csv', 'r') as csvfile:
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

        # Print the package
        print(package)

        # Add the package to the dispatcher
        dispatcher.packages.append(package)