from datetime import timedelta

class Truck:
    speed = 18

    #init
    def __init__(self, truck_id, dispatcher, queued_package_ids, driver_index):
        self.truck_id = truck_id
        self.queued_package_ids = queued_package_ids #list of package ids to be delivered
        self.delayed_package_ids = [] #list of package ids that have a delayed address or have a wrong address
        self.delivered_package_ids = [];
        self.miles = 0 #miles traveled
        self.last_package_delivered = None #package object 
        self.driver_index = driver_index #driver index from dispatch driver list (indicates which driver is assigned to this truck)
        self.status = "At Hub" #status of the truck (At Hub, In Transit, etc.)
        self.dispatcher = dispatcher
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

            #this is to prevent the truck from moving faster than the live time
            theoretical_delivery_time = self.time + timedelta(minutes=(distance / self.speed * 60))
            if theoretical_delivery_time >= self.dispatcher.live_time:
                print("Truck #" + str(self.truck_id) + " is waiting for live time to catch up to theoretical delivery time\n")

                #update truck status
                self.status = f"On the way to HUB (ETA: {theoretical_delivery_time.strftime('%I:%M %p')})"

                return

            self.time += timedelta(minutes=time_to_travel)
            self.current_loc_index = 0
            self.miles += distance
            self.dispatcher.current_time = self.time
            self.status = "At Hub"
            

    #gets the next available truck that has packages to deliver (if any)
    def get_available_truck(self):
        for truck in self.dispatcher.trucks:
            if truck.driver_index is None and len(truck.queued_package_ids) > 0 and truck.get_id() != self.truck_id:
                return truck
            
        return None
    
    #requeues delayed packages that are ready to be delivered
    def re_queue_delayed_packages(self):
        
        #packages to requeue
        packages_to_requeue = []

        #for id in self.delayed_package_ids:
        for i in range(len(self.delayed_package_ids)):
            package = self.dispatcher.package_table.get(self.delayed_package_ids[i])

            do_update = False
            
            if package.delayed_address_time is not None and (package.delayed_address_time <= self.dispatcher.live_time.time()):
                do_update = True

            if package.delayed_arrival_time is not None and (package.delayed_arrival_time <= self.dispatcher.live_time.time()):
                do_update = True

            #if the package has a delayed address time that is less than the current time, then it is ready to be delivered
            if do_update:

                if package.delayed_arrival_time is not None:
                    #update status to At Hub
                    package.set_status("At Hub")
                else:
                    
                    #if truck is at the hub, update status to At Hub
                    if self.current_loc_index == 0:
                        package.set_status("At Hub")
                    else:
                        print("Adding package " + str(package.get_id()) + " back to truck " + str(self.truck_id) + " queue with delayed address\n")
                        package.set_status("In Transit") #update package delivery status    
                
                if package.delayed_address is not None:
                    #update the the package address to the delayed address
                    package.set_address(package.delayed_address)
                    package.set_delayed_matrix_index() #update the package matrix index based on the new address

                #add the package id back to the queued package ids
                self.queued_package_ids.append(package.get_id())
                
                #add the package to the packages to requeue so that it can be removed from the delayed packages
                packages_to_requeue.append(package)

                #report time to truck
                self.time = self.dispatcher.current_time

        #remove packages from delayed packages
        for package in packages_to_requeue:
            self.delayed_package_ids.remove(package.get_id())


    #dequeue delayed packages that are not ready to be delivered yet
    def de_queue_delayed_packages(self):
        
        #for every queued package, check if it has a delayed address or delayed arrival time
        for package_id in self.queued_package_ids:
            package = self.dispatcher.package_table.get(package_id)

            if package.get_status() == "Delayed":
                #if package has a delayed address, and is not ready to be sent, set it a side and continue to next package
                if package.delayed_address is not None: #and package.get_status() != "In Transit":
                    #add the package to delayed address packages
                    self.delayed_package_ids.append(package_id)
                    

                #if package has delayed_arrival_time, and is ready to be sent, update the package address and matrix index
                if package.delayed_arrival_time is not None: #and package.get_status() != "At Hub":
                
                    #add the package to delayed address packages
                    self.delayed_package_ids.append(package_id)

        
        #for every delayed package, remove from queued packages
        for package_id in self.delayed_package_ids:
            if package_id in self.queued_package_ids:
                self.queued_package_ids.remove(package_id)
 


    #deliver packages
    def truck_step(self):
        print("Truck #" + str(self.truck_id) + " Step------------------------------------\n")

        self.de_queue_delayed_packages()

        #requeue delayed packages that are ready to be delivered
        self.re_queue_delayed_packages()

        #if truck has driver 
        if self.driver_index is not None:

            #if there are no more packagaes to deliver in the queue
            if len(self.queued_package_ids) == 0: 
                print("No packages to deliver for truck #" + str(self.truck_id) + "\n")
                
                available_truck = self.get_available_truck()

                #if not at hub, go back home
                if self.current_loc_index != 0:
                    self.go_back_to_hub(); #temp comment: not used by truck 2
                    
                    if available_truck != None:
                        #update the time on the available truck to the current time of this truck
                        available_truck.time = self.time
                    
                    return
                
                
                if available_truck is not None:
                    #print("Truck #" + str(available_truck.get_id()) + " is ready for transit, assigning driver: " + str(self.driver_index + 1))
                    print(f"Assigning Driver: {self.driver_index + 1} to Truck #{available_truck.get_id()}\n")

                    #assign new truck to driver
                    self.dispatcher.drivers[self.driver_index].truck = available_truck
                    
                    #assign driver of this truck to the truck with no driver
                    self.dispatcher.drivers[self.driver_index].truck.driver_index = self.driver_index
                    
                    #remove driver from this truck
                    self.driver_index = None

                    #update the time of the new truck to the current time of this truck
                    available_truck.time = self.time
                    available_truck.dispatcher.current_time = self.time
                    
                    return

                return

            #find closest package
            min_distance = 9999; #init min distance to a high number
            closest_package = None

            #find closest package
            for package_id in self.queued_package_ids:
                package = self.dispatcher.package_table.get(package_id)

                #calculate distance from current location to package address
                distance = self.dispatcher.distance_matrix[self.current_loc_index][package.dist_matrix_index]

                #if the distance found in the distance matrix is less than the current min distance, update the min distance and 
                #the closest package
                if  distance < min_distance:
                    min_distance = self.dispatcher.distance_matrix[self.current_loc_index][package.dist_matrix_index]
                    closest_package = package

            #move truck to closest package, only move if the live time is less than or equal to the package calculated delivery time
            theoretical_delivery_time = self.time + timedelta(minutes=(min_distance / self.speed * 60))

            #this is to prevent the truck from moving faster than the live time 
            if theoretical_delivery_time >= self.dispatcher.live_time:

                #update truck status
                eta = theoretical_delivery_time.strftime("%I:%M %p")
                self.status = f"On the way to " + str(closest_package.get_address()) + " (ETA: " + eta + ") "

                print("Truck #" + str(self.truck_id) + " is " + self.status + "\n")

                return
            

            print(f"Moving to Next Location: {closest_package.get_address()} (Package ID: {closest_package.get_id()}) : {min_distance} miles away\n")

            time_to_travel = min_distance / self.speed * 60 #calculate time to travel to closest package
            self.time += timedelta(minutes=time_to_travel) #update truck time
            self.dispatcher.current_time = self.time
            self.dispatcher.delivered_package_ids.append(closest_package.get_id()) #push package to delivered packages from the dispatcher
            self.delivered_package_ids.append(closest_package.get_id())
            closest_package.set_status("Delivered") #update package delivery status
            self.last_package_delivered = closest_package.get_id() #update last package delivered
            self.miles += min_distance #update truck miles
            self.current_loc_index = closest_package.dist_matrix_index #update truck location index
            closest_package.set_delivery_time(self.time) #update package delivery time
            self.queued_package_ids.remove(closest_package.get_id()) #pop closest package off the truck queue

            #step again, if there are more packages to deliver at the same time
            self.truck_step()
            

        

        