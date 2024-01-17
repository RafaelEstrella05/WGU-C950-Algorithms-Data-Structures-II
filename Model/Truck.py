from datetime import datetime
from datetime import timedelta
from datetime import datetime
#Truck class

class Truck:
    speed = 18
    loading_address = "4001 South 700 East, Salt Lake City, UT 84107"

    #init
    def __init__(self, truck_id, dispatcher):
        self.truck_id = truck_id
        self.queued_packages = [] #list of packages to be delivered
        self.miles = 0 #miles traveled
        self.last_package_delivered = None #package object 
        self.driver = None
        
        # set time to today's date at 8:00 AM
        self.time = datetime.combine(datetime.today(), datetime.strptime("8:00 AM", "%I:%M %p").time())
        self.current_location = self.loading_address
        self.current_loc_index = 0 #for distance matrix
        self.dispatcher = dispatcher

    def update_current_location(self, current_address, current_loc_index):
        self.current_location = current_address
        self.current_loc_index = current_loc_index

    def get_id(self):
        return self.truck_id

    #assign package to truck
    def assign_package(self, package):
        self.queued_packages.append(package)

    def print_truck_status(self):
        print("Truck ID:", self.truck_id)
        print("Miles:", self.miles)
        print("Last Package Delivered:", self.last_package_delivered)
        print("Dispatcher Time:", self.dispatcher.current_time)
        print("Last Delivered Time:", self.time)
        print("Current Location:", self.current_location)
        if(self.driver is not None):
            print("Driver:", self.dispatcher.drivers[self.driver]["name"])
        else:
            print("Driver: None")

    def truck_step(self):
        print("Truck #" + str(self.truck_id) + " Step")

        if self.truck_id == 2:
            print();

        delayed_packages = []

        
        if len(self.queued_packages) == 0:
            print("No packages to deliver for truck #" + str(self.truck_id) + "\n")

            #go back home if not already, calculate time to travel and update truck time and current location
            if self.current_location != self.loading_address:
                distance = self.dispatcher.distance_matrix[self.current_loc_index][0]
                time_to_travel = distance / self.speed * 60
                self.time += timedelta(minutes=time_to_travel)
                self.current_location = self.loading_address
                self.current_loc_index = 0
                self.miles += distance
                self.dispatcher.current_time = self.time

            #check if there are any trucks available with no driver that have packages to deliver
            for truck in self.dispatcher.trucks.values():
                if truck.driver is None and len(truck.queued_packages) > 0:
                    print("Truck #" + str(truck.get_id()) + " has no driver but has packages to deliver")

                    #assign new truck to driver
                    self.dispatcher.drivers[self.driver]["truck"] = truck
                    
                    #assign driver of this truck to the truck with no driver
                    truck.driver = self.driver

                    
                    return
            
            #otherwise remove driver from truck
            self.dispatcher.drivers[self.driver]["truck"] = None

            self.driver = None

            return
        
        min_distance = 999;

        #find current location index from location labels
        for index, location in self.dispatcher.location_labels.items():
            if location == self.current_location:
                self.current_loc_index = index
                self.current_location = location
                break

        closest_package = None;
        
        #print("finding closest distance to (" + str(self.current_location) + ")...\n")

        #find closest package
        for package in self.queued_packages:

            #if package has a delayed address, skip it
            if package.delayed_address is not None:
                delayed_packages.append(package)

                #if the current time is past the delayed address time, update the package address to the delayed address so that it is ready to be delivered
                if self.dispatcher.current_time >= datetime.combine(datetime.today(), package.delayed_address_time):
                    print("Package #" + str(package.get_id()) + " has a delayed address and it is past the delayed address time")

                    #update package address and delivery status
                    package.set_address(package.delayed_address)
                    package.delayed_address = None
                    package.delayed_address_time = None

                    #update package distance matrix index
                    for index, location in self.dispatcher.location_labels.items():
                        if location == package.get_address():
                            package.dist_matrix_index = index
                            break
                
                #continue

            distance = self.dispatcher.distance_matrix[self.current_loc_index][package.dist_matrix_index]

            #if the distance found in the distance matrix is less than the current min distance, update the min distance and 
            #the closest package
            if  distance < min_distance:
                min_distance = self.dispatcher.distance_matrix[self.current_loc_index][package.dist_matrix_index]
                closest_package = package

        if closest_package is None:
            print("No packages to deliver for truck #" + str(self.truck_id) + "\n")
            return

        #print "closest package to <Package ID> : <Package Address> is package <Package ID> : <Package Address> :  <Distance> miles away"
        print("\nCLOSEST package to (" + str(self.current_location)  + ") is package " + str(closest_package.get_id()) + " : (" + closest_package.get_address() + ") : " + str(min_distance) + " miles away\n")

        time_to_travel = min_distance / self.speed * 60 #calculate time to travel to closest package
        self.time += timedelta(minutes=time_to_travel) #update truck time
        self.dispatcher.current_time = self.time
        self.dispatcher.delivered_packages.append(closest_package) #push package to delivered packages from the dispatcher
        closest_package.set_delivery_status("Delivered") #update package delivery status
        self.last_package_delivered = closest_package #update last package delivered
        self.miles += min_distance #update truck miles
        self.current_location = closest_package.get_address() #update truck location
        self.current_loc_index = closest_package.dist_matrix_index #update truck location index
        closest_package.set_delivery_time(self.time) #update package delivery time
        self.queued_packages.remove(closest_package) #pop closest package off the truck queue




            

        

        