
'''
Dispatcher is in charge of managing the trucks and drivers that will be delivering the packages.
'''
from datetime import datetime, timedelta

from Model.Truck import Truck  
from Model.Driver import Driver 
from Model.HashTable import HashTable

class Dispatcher:
    loading_address = "4001 South 700 East,  Salt Lake City, UT 84107"
    loading_address_index = 0

    #live_time is the current time of the dispatcher, starting at 8:00 AM
    live_time = datetime.combine(datetime.today(), datetime.strptime("8:00 AM", "%I:%M %p").time())

    package_table = HashTable(); #list of packages to be delivered #FIX ME: queued_packages should be a hashmap of package_id -> package
    delivered_package_ids = []

    #location labels
    location_labels = [] 

    #distance matrix (Complete Graph)
    distance_matrix = [];

    #init (hardcoded data)
    def __init__(self):

        self.trucks = [
        Truck(1, self, [29, 1, 40, 27, 35, 7, 4, 10, 5, 2, 33, 21, 31], 0), #Truck(truck_id, dispatcher, queued_package_ids, driver_index)
        Truck(2, self, [15, 13, 30, 20, 37, 14, 16, 34, 18, 19, 39, 36, 3, 8, 9, 38], 1),
        Truck(3, self, [6, 32, 25, 11, 28, 17, 12, 24, 23, 26, 22], None)
        ]

        self.drivers = [
            Driver(1, "Billy", self.trucks[0]),
            Driver(2, "Bob", self.trucks[1])
        ]

    #load distance data
    def load_distance_data(self, location_labels, distance_matrix):
        self.location_labels = location_labels
        self.distance_matrix = distance_matrix
        
    #For every truck taken by a driver, move the truck one step.
    def dispatchStep(self):

        #add one minute to the live time
        self.live_time = self.live_time + timedelta(minutes=1)

        #for every truck, move the truck one step.
        for truck in self.trucks:

            #requeue delayed packages that are ready to be delivered
            truck.re_queue_delayed_packages()

            #if truck has driver 
            if truck.driver_index is not None:
            
                #step the truck
                truck.move_truck()

                #if truck is at the hub and has no more packages to deliver, then the truck is done and can look for another truck that needs a driver
                if truck.current_loc_index == 0 and len(truck.queued_package_ids) == 0 and len(truck.delayed_package_ids) == 0:
                    
                    available_truck = self.get_next_available_truck(truck)
            
                    if available_truck is not None:
                        #print("Truck #" + str(available_truck.get_id()) + " is ready for transit, assigning driver: " + str(self.driver_index + 1))
                        print(f" ({self.live_time.strftime('%I:%M%p')}) Assigning Driver: {truck.driver_index + 1} to Truck #{available_truck.get_id()}")

                        #assign new truck to driver
                        self.drivers[truck.driver_index].truck = available_truck
                        
                        #assign driver of this truck to the truck with no driver
                        self.drivers[truck.driver_index].truck.driver_index = truck.driver_index
                        
                        #remove driver from this truck
                        truck.driver_index = None

                        #update the time of the new truck to the current time of this truck
                        available_truck.time = truck.time

                
                
                #change package status based on truck status
                if "En Route to" in truck.status:
                    truck.update_all_package_status("En Route")
                else:
                    truck.update_all_package_status("At Hub")


        #gets the next available truck that has packages to deliver (if any)
    def get_next_available_truck(self, current_truck):
        for truck in self.trucks:
            if truck.driver_index is None and len(truck.queued_package_ids) > 0 and truck.get_id() != current_truck.truck_id:
                return truck
            
        return None


    #check if all trucks are at the hub
    def is_dispatch_complete(self):

        #if there are no more packages to be delivered and trucks are at the hub, then the dispatch is complete
        for truck in self.trucks:
            if len(truck.queued_package_ids) > 0:
                return False
            if truck.current_loc_index != 0:
                return False
            
        return True
    

    def get_location_index(self, lookup_location):

        for i in range(len(self.location_labels)):
            if self.location_labels[i] == lookup_location:
                return i

        return None


    def de_queue_unready_packages(self):
        #for every truck in the dispatcher, dequeue any packages that are not ready to be delivered
        for truck in self.trucks:
            truck.de_queue_delayed_packages()

    def print_all_truck_status(self):
        print();
        print("STATUS FOR TRUCKS: ")
        for truck in self.trucks:

            truck.print_truck_status();
            print(f"TRUCK {truck.truck_id} HAS {len(truck.queued_package_ids)} PACKAGES REMAINING:", end=" [")
            #beside the packages remaining, print the package id of each package remaining
            for package_id in truck.queued_package_ids:
                package = self.package_table.get(package_id)
                print(package.get_id(), end=", ")
            print("]")
            #print delayed address packages
            print("Delayed Address Packages: ", end=" [")
            for package_id in truck.delayed_package_ids:
                package = self.package_table.get(package_id)
                print(package.get_id(), " (wrong address)", end=", ")

            print("]")
            print();
    

    def print_all_truck_delivered_packages(self):
        print();
        print("ALL TRUCK DELIVERED PACKAGES: ")

        if len(self.delivered_package_ids) == 0:
            print("No packages have been delivered")
            return
        for package_id in self.delivered_package_ids:
            package = self.package_table.get(package_id)
            print(package)

    def print_num_delivered_packages(self):
        print();
        print("NUMBER OF DELIVERED PACKAGES: ", len(self.delivered_package_ids), end=" [")
        
        for package_id in self.delivered_package_ids:
            package = self.package_table.get(package_id)
            print(package.get_id(), end=", ")
        print("]")
        print();



 


