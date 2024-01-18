
'''
The dispatcher is responsible for controlling the steps trucks take to deliver packages.
Each step involves a truck moving from one unvisited location to another.  

The dispatcher is also responsible for keeping track of the time of day, and updating the delivery status of packages.
'''

from Model.Truck import Truck  # Import the Truck module correctly

# Constructor
class Dispatcher:

    queued_packages = [] #list of packages to be delivered 
    delivered_packages = [] #list of packages that have been delivered 

    #location labels
    location_labels = {} 

    #distance matrix (Complete Graph)
    distance_matrix = [];

    #drivers that are available
    drivers = {}

    #trucks that are available
    trucks = {}

    current_time = None
    
    #load distance data
    def load_distance_data(self, location_labels, distance_matrix):
        self.location_labels = location_labels
        self.distance_matrix = distance_matrix

    
    #load truck data
    def load_package(self, package):

        #if the length of queued packages is 0, just add the package
        if len(self.queued_packages) == 0:
            self.queued_packages.append(package)
            return

        # Find the index to insert the new package
        index = 0
        while index < len(self.queued_packages) and self.queued_packages[index].get_id < package.get_id:
            index += 1

        # Insert the new package at the correct index
        self.queued_packages.insert(index, package)

    #finds package by id
    def find_queued_package(self, package_id):
        # Binary search to find the package
        left = 0
        right = len(self.queued_packages) - 1

        while left <= right:
            mid = (left + right) // 2
            if int(self.queued_packages[mid].get_id) == int(package_id):
                package = self.queued_packages[mid]
                break
            elif int(self.queued_packages[mid].get_id) < int(package_id):
                left = mid + 1
            else:
                right = mid - 1
        else:
            package = None

        return package


    def initDrivers(self):
        #hardcoded list of drivers
        self.drivers = {
            1: {
                "name": "Driver 1",
                "truck": None
            },
            2: {
                "name": "Driver 2",
                "truck": None
            }
        }
        
    def initTrucks(self):
        #hardcoded list of trucks
        self.trucks = {
            1: Truck(1, self),
            2: Truck(2, self),
            3: Truck(3, self)
        }
        
    def initTruckDrivers(self):
        #for every driver, assign a truck
        for driver_id in self.drivers:
            driver = self.drivers[driver_id]
            truck = self.trucks[driver_id] #not the best way to do this, but it works
            driver["truck"] = truck
            truck.driver = driver_id;
            
    
    #hardcoded function
    def initPackages(self):  # Add missing self parameter

        print("Assigning packages to trucks...")

        # hardcoded list of package ids to be delivered by each truck with a driver
        truck1_package_ids = [29, 1, 40, 27, 35, 7, 4, 10]
        truck2_package_ids = [15, 13, 30, 20, 37, 14, 16, 34, 18, 19, 39, 36, 3, 8, 9, 38]
        truck3_package_ids = [6, 32, 25, 21, 2, 33, 11, 28, 17, 31, 12, 5, 24, 23, 26, 22];

        trucks_list = [truck1_package_ids, truck2_package_ids, truck3_package_ids]

        for i in range(0, len(trucks_list)):
            truck = self.trucks[i + 1]  # Add missing self parameter
            for j in range(0, len(trucks_list[i])):
                package = self.find_queued_package(trucks_list[i][j]) 



                if package is not None:
                    print("Assigning package ", package.get_id(), " to truck ", truck.get_id());
                    self.assign_package_to_truck(package.get_id(), truck)
                    self.queued_packages.remove(package)
                    print();




    #assign package to truck with id
    def assign_package_to_truck(self, package_id, truck):

            

        package = self.find_queued_package(package_id)  # Add missing self parameter

        #find matrix index of package address
        package_address_combined = package.details["address"] + " (" + package.details["zip_code"] + ")"
        

        #find distance matrix index of package address for easy lookup
        package_address_index = -1
        #look through each location label, if the value is equal to the package_address_combined, then we have found the index
        for location_index in self.location_labels:
            if self.location_labels[location_index] == package_address_combined:
                package_address_index = location_index
                break

        if(package_address_index == -1):
            print("ERROR: Package address index not found.")
            return

        print("Package address: ", (package_address_combined) + ", Matrix Index: ", package_address_index);

        if package_address_index != -1:
            package.dist_matrix_index = package_address_index
            truck.assign_package(package)
            #package.set_truck(truck)
            package.set_delivery_status("Loaded on Truck")


    '''
    For every truck taken by a driver, move the truck one step.
    '''
    def dispatchStep(self):
        
        #for every driver that has a truck assigned, move the truck one step.
        for driver_id in self.drivers:
            driver = self.drivers[driver_id]
            truck = driver["truck"]
            
            if truck is not None:
                truck.truck_step()


    def is_dispatch_complete(self):
        #if there are no more packages to be delivered, then the dispatch is complete
        #search through each truck to make sure no packages are left
        for truck_id in self.trucks:
            truck = self.trucks[truck_id]
            if len(truck.queued_packages) > 0:
                return False
            
        return True



    def print_all_truck_status(self):
        print();
        print("STATUS FOR TRUCKS: ")
        for truck_id in self.trucks:
            truck = self.trucks[truck_id]
            truck.print_truck_status();
            print(f"TRUCK {truck_id} HAS {len(truck.queued_packages)} PACKAGES REMAINING:", end=" [")
            #beside the packages remaining, print the package id of each package remaining
            for package in truck.queued_packages:
                print(package.get_id(), end=", ")
            print("]")
            #print delayed address packages
            print("Delayed Address Packages: ", end=" [")
            for package in truck.delayed_address_packages:
                print(package.get_id(), " is delayed due to wrong address", end=", ")

            print("]")
            print();
    

    def print_all_truck_delivered_packages(self):
        print();
        print("ALL TRUCK DELIVERED PACKAGES: ")

        if len(self.delivered_packages) == 0:
            print("No packages have been delivered")
            return
        for package in self.delivered_packages:
            print(package)

    def print_num_delivered_packages(self):
        print();
        print("NUMBER OF DELIVERED PACKAGES: ", len(self.delivered_packages), end=" [")
        
        for package in self.delivered_packages:
            print(package.get_id(), end=", ")
        print("]")
        print();



 


