from datetime import datetime
from datetime import timedelta
from datetime import datetime
#Truck class

class Truck:
    speed = 18

    #init
    def __init__(self, truck_id, dispatcher, queued_package_ids, driver_index):
        self.truck_id = truck_id
        self.queued_package_ids = queued_package_ids #list of package ids to be delivered
        self.delayed_package_ids = [] #list of package ids that have a delayed address or have a wrong address

        self.miles = 0 #miles traveled
        self.last_package_delivered = None #package object 
        self.driver_index = driver_index #driver index from dispatch driver list (indicates which driver is assigned to this truck)
        
        self.dispatcher = dispatcher

        # set time to today's date at 8:00 AM
        self.time = self.dispatcher.current_time
        self.current_loc_index = 0 #for distance matrix

    def get_id(self):
        return self.truck_id

    def print_truck_status(self):
        driver_text = None
        if(self.driver_index is not None):
            driver_text = self.driver_index + 1
        else:
            driver_text = "None"
        print("Truck ID:", self.truck_id, ", Driver:", driver_text, ", Truck Miles:", self.miles)
        print("Last Package Delivered:", self.dispatcher.package_table.get(self.last_package_delivered))
        print("Dispatcher Time:", self.dispatcher.current_time)
        print("Last Delivered Time:", self.time)
        print("Current Location:", str(self.dispatcher.location_labels[self.current_loc_index]))

    #updates the status of the truck to be in the loading dock
    def go_back_to_hub(self):
        #go back home first if not already, calculate time to travel and update truck time and current location
        if self.current_loc_index != self.dispatcher.loading_address_index:
            #print "moving truck from <Current Location> to the hub : <Distance> miles away"
            print("\nMoving truck from (" + str(self.dispatcher.location_labels[self.current_loc_index]) + ") to the HUB : " + str(self.dispatcher.distance_matrix[self.current_loc_index][0]) + " miles away\n")
            distance = self.dispatcher.distance_matrix[self.current_loc_index][0]
            time_to_travel = distance / self.speed * 60
            self.time += timedelta(minutes=time_to_travel)
            self.current_loc_index = 0
            self.miles += distance
            self.dispatcher.current_time = self.time

    #gets the next available truck that has packages to deliver (if any)
    def get_available_truck(self):
        for truck in self.dispatcher.trucks:
            if truck.driver_index is None and len(truck.queued_package_ids) > 0 and truck.get_id() != self.truck_id:
                return truck
            
        return None
    
    #requeues delayed packages that are ready to be delivered
    def re_queue_delayed_packages(self):
        
        for id in self.delayed_package_ids:
            package = self.dispatcher.package_table.get(id)

            do_update = False
            
            #if len(self.queued_packages) == 0:
            if len(self.queued_package_ids) == 0:
                do_update = True

            if package.delayed_address_time is not None and (package.delayed_address_time <= self.dispatcher.current_time.time() or package.delayed_address_time <= self.time.time()):
                do_update = True

            #if the package has a delayed address time that is less than the current time, then it is ready to be delivered
            if do_update:

                self.go_back_to_hub();

                #print "adding package <id> back to truck <id> queue with delayed address"
                print("Adding package " + str(package.get_id()) + " back to truck " + str(self.truck_id) + " queue with delayed address\n")
                package.set_status("In Transit") #update package delivery status

                #update the the package address to the delayed address
                package.set_address(package.delayed_address)
                package.set_delayed_matrix_index() #update the package matrix index based on the new address

                #add the package id back to the queued package ids
                self.queued_package_ids.append(package.get_id())
                #remove from delayed address packages
                self.delayed_package_ids.remove(package.get_id())


    #move truck one step
    def truck_step(self):
        print("Truck #" + str(self.truck_id) + " Step")
        
        #if there are any delayed packages that are ready to be delivered, requeue them to queued package ids
        self.re_queue_delayed_packages();
        
        #if there are no more packagaes to deliver in the queue
        if len(self.queued_package_ids) == 0: 
            print("No packages to deliver for truck #" + str(self.truck_id) + "\n")


            #go back home if not already, calculate time to travel and update truck time and current location
            self.go_back_to_hub();

            #get next available truck
            available_truck = self.get_available_truck();
                
            if available_truck is not None:
                print("Truck #" + str(available_truck.get_id()) + " is ready for transit, assigning driver: " + str(self.driver_index + 1))

                #assign new truck to driver
                self.dispatcher.drivers[self.driver_index].truck = available_truck
                
                #assign driver of this truck to the truck with no driver
                self.dispatcher.drivers[self.driver_index].truck.driver_index = self.driver_index
                
                #remove driver from this truck
                self.driver_index = None
                
                return
            
            #otherwise remove driver from truck
            self.dispatcher.drivers[self.driver_index].truck = None
            self.driver_index = None

            return
        

        #find closest package
        min_distance = 9999; #init min distance to a high number
        closest_package = None

        #find closest package
        for package_id in self.queued_package_ids:
            package = self.dispatcher.package_table.get(package_id)

            #if package has a delayed address, and is not ready to be sent, set it a side and continue to next package
            if package.delayed_address is not None and package.get_status() != "In Transit":
                #add the package to delayed address packages
                self.delayed_package_ids.append(package_id)
                #remove from queued packages
                self.queued_package_ids.remove(package_id)
                continue

            #calculate distance from current location to package address
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
        print("\nMoving truck from (" + str(self.dispatcher.location_labels[self.current_loc_index]) + ") to (" + str(closest_package.get_address()) + ") (" + str(closest_package.get_id()) + ") : " + str(min_distance) + " miles away\n")

        #move truck to closest package
        time_to_travel = min_distance / self.speed * 60 #calculate time to travel to closest package
        self.time += timedelta(minutes=time_to_travel) #update truck time
        self.dispatcher.current_time = self.time
        self.dispatcher.delivered_package_ids.append(closest_package.get_id()) #push package to delivered packages from the dispatcher
        closest_package.set_status("Delivered") #update package delivery status
        self.last_package_delivered = closest_package.get_id() #update last package delivered
        self.miles += min_distance #update truck miles
        self.current_loc_index = closest_package.dist_matrix_index #update truck location index
        closest_package.set_delivery_time(self.time) #update package delivery time
        self.queued_package_ids.remove(closest_package.get_id()) #pop closest package off the truck queue




            

        

        