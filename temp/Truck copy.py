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
        self.delayed_address_packages = [] #list of packages that have a delayed address
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
        driver_text = None
        if(self.driver is not None):
            driver_text = self.driver
        else:
            driver_text = "None"
        print("Truck ID:", self.truck_id, ", Driver:", driver_text, ", Truck Miles:", self.miles)
        print("Last Package Delivered:", self.last_package_delivered)
        print("Dispatcher Time:", self.dispatcher.current_time)
        print("Last Delivered Time:", self.time)
        print("Current Location:", self.current_location)


    def truck_step(self):
        print("Truck #" + str(self.truck_id) + " Step")

        
        #loop through delayed address packages and check if any of them have a delayed address time that is less than the current time
        #this is to check if any of the packages have a delayed address that is ready to be delivered
        for package in self.delayed_address_packages:

            do_update = False
            
            if len(self.queued_packages) == 0:
                do_update = True

            if package.delayed_address_time is not None and (package.delayed_address_time <= self.dispatcher.current_time.time() or package.delayed_address_time <= self.time.time()):
                do_update = True

            #if the package has a delayed address time that is less than the current time, then it is ready to be delivered
            if do_update:

                #go back home first if not already, calculate time to travel and update truck time and current location
                if self.current_location != self.loading_address:
                    #print "moving truck from <Current Location> to the hub : <Distance> miles away"
                    print("\nMoving truck from (" + str(self.current_location) + ") to the HUB : " + str(self.dispatcher.distance_matrix[self.current_loc_index][0]) + " miles away\n")
                    distance = self.dispatcher.distance_matrix[self.current_loc_index][0]
                    time_to_travel = distance / self.speed * 60
                    self.time += timedelta(minutes=time_to_travel)
                    self.current_location = self.loading_address
                    self.current_loc_index = 0
                    self.miles += distance
                    self.dispatcher.current_time = self.time


                #print "adding package <id> back to truck <id> queue with delayed address"
                print("Adding package " + str(package.get_id()) + " back to truck " + str(self.truck_id) + " queue with delayed address\n")
                

                package.details["delivery_status"] = "In Transit"

                #update the the package address to the delayed address
                package.set_address(package.delayed_address)

                #update the package's distance matrix index
                for index, location in self.dispatcher.location_labels.items():
                    if location == package.get_address():
                        package.dist_matrix_index = index
                        break

                #add the package back to the queued packages
                self.queued_packages.append(package)
                #remove from delayed address packages
                self.delayed_address_packages.remove(package)
                
                #return
        

        if len(self.queued_packages) == 0: #if there are no more packagaes to deliver in the queue
            print("No packages to deliver for truck #" + str(self.truck_id) + "\n")


            #go back home if not already, calculate time to travel and update truck time and current location
            if self.current_location != self.loading_address:

                #print "moving truck from <Current Location> to the hub : <Distance> miles away"
                print("\nMoving truck from (" + str(self.current_location) + ") to the HUB : " + str(self.dispatcher.distance_matrix[self.current_loc_index][0]) + " miles away\n")
                distance = self.dispatcher.distance_matrix[self.current_loc_index][0]
                time_to_travel = distance / self.speed * 60
                self.time += timedelta(minutes=time_to_travel)
                self.current_location = self.loading_address
                self.current_loc_index = 0
                self.miles += distance
                self.dispatcher.current_time = self.time

            #check if there are any trucks available with no driver that have packages to deliver
            for truck in self.dispatcher.trucks.values():
                if truck.driver is None and len(truck.queued_packages) > 0 and truck.get_id() != self.truck_id:
                    print("Truck #" + str(truck.get_id()) + " has no driver but has packages to deliver")

                    #assign new truck to driver
                    self.dispatcher.drivers[self.driver]["truck"] = truck
                    
                    #assign driver of this truck to the truck with no driver
                    self.dispatcher.drivers[self.driver]["truck"].driver = self.driver

                    self.driver = None
                    
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

        #find closest package
        for package in self.queued_packages:

            #if package has a delayed address, and is not ready, set it a side and continue to next package
            if package.delayed_address is not None and package.details["delivery_status"] != "In Transit":
                #add the package to delayed address packages
                self.delayed_address_packages.append(package)
                #remove from queued packages
                self.queued_packages.remove(package)
                continue


            distance = self.dispatcher.distance_matrix[self.current_loc_index][package.dist_matrix_index]

            #if the distance found in the distance matrix is less than the current min distance, update the min distance and 
            #the closest package
            if  distance < min_distance:
                min_distance = self.dispatcher.distance_matrix[self.current_loc_index][package.dist_matrix_index]
                closest_package = package

        if closest_package is None:
            print("No packages to deliver for truck #" + str(self.truck_id) + "\n")
            return

        #print "moving truck from <Current Location> to <Package Address> (<package ID>)) : <Distance> miles away"
        print("\nMoving truck from (" + str(self.current_location) + ") to (" + str(closest_package.get_address()) + ") (" + str(closest_package.get_id()) + ") : " + str(min_distance) + " miles away\n")

        ###MOVE TRUCK TO CLOSEST PACKAGE
        #calculate time to travel to closest package so that we can update the truck time
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




            

        

        