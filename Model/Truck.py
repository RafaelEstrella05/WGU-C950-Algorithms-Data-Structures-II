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
        self.status = "At Hub" #status of the truck (At Hub, En Route, etc.)
        self.dispatcher = dispatcher
        self.time = self.dispatcher.live_time
        self.current_loc_index = 0 #for distance matrix

        print(f"({self.dispatcher.live_time.strftime('%I:%M%p')}) Truck #{self.truck_id} | Location: HUB | Total Miles: 0")


    def get_id(self):
        return self.truck_id

    def print_truck_status(self):
        driver_text = None
        if(self.driver_index is not None):
            driver_text = self.driver_index + 1
        else:
            driver_text = "None"
        print("Truck ID:", self.truck_id, ", Driver:", driver_text, ", Truck Miles:", self.miles)
        print("Status:", self.status)
        print("Last Package Delivered:", self.dispatcher.package_table.get(self.last_package_delivered))
        print("Last Reported Time:", self.time)
        print("Current Location:", str(self.dispatcher.location_labels[self.current_loc_index]))

    #updates the status of the truck to be in the loading dock
    def return_to_hub(self):

        
        #go back home first if not already, calculate time to travel and update truck time and current location
        if self.current_loc_index != self.dispatcher.loading_address_index:
            distance = self.dispatcher.distance_matrix[self.current_loc_index][0]
            time_to_travel = distance / self.speed * 60

            #this is to prevent the truck from moving faster than the live time
            delivery_eta = self.time + timedelta(minutes=(distance / self.speed * 60))
            if delivery_eta >= self.dispatcher.live_time + timedelta(minutes=1):

                #update truck status
                self.status = f"En Route to HUB (ETA: {delivery_eta.strftime('%I:%M %p')})"

                #print("Truck #" + str(self.truck_id) + " is " + self.status + "\n")

                return
            
            print(f"({self.dispatcher.live_time.strftime('%I:%M%p')}) Truck #{self.truck_id} | Location: HUB | Distance Traveled: {distance} | Total Miles: {self.miles + distance}")

            self.time += timedelta(minutes=time_to_travel)
            self.current_loc_index = 0
            self.miles += distance
            self.status = "At Hub"
            
    
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

                    #print "package has arrived at the hub, updating status to At Hub"
                    print(f"({self.dispatcher.live_time.strftime('%I:%M %p')}) Truck #{self.truck_id} Package #{package.get_id()} has arrived at the hub")

                    #update status to At Hub
                    package.set_status("At Hub")
                else:
                    
                    #if truck is at the hub, update status to At Hub
                    if self.current_loc_index == 0:
                        package.set_status("At Hub")
                    else:
                        print(f"({self.dispatcher.live_time.strftime('%I:%M %p')}) Adding delayed package " + str(package.get_id()) + " back to truck #" + str(self.truck_id) + " queue")
                        package.set_status("En Route") #update package delivery status    
                
                if package.delayed_address is not None:
                    #update the the package address to the delayed address
                    package.set_address(package.delayed_address)
                    package.set_delayed_matrix_index() #update the package matrix index based on the new address

                #add the package id back to the queued package ids
                self.queued_package_ids.append(package.get_id())
                
                #add the package to the packages to requeue so that it can be removed from the delayed packages
                packages_to_requeue.append(package)

                #report time to truck
                self.time = self.dispatcher.live_time

        #remove packages from delayed packages
        for package in packages_to_requeue:
            self.delayed_package_ids.remove(package.get_id())


    #dequeue delayed packages that are not ready to be delivered yet
    def de_queue_delayed_packages(self):
        
        #for every queued package, check if it has a delayed address or delayed arrival time
        for package_id in self.queued_package_ids:
            package = self.dispatcher.package_table.get(package_id)

            if package.get_status() == "Delayed":
                #if package has a delayed address, and is not ready to be sent, set it a side and continue to nxt package
                if package.delayed_address is not None: #and package.get_status() != "En Route":
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


    def update_all_package_status(self, status):
        for package_id in self.queued_package_ids:
            package = self.dispatcher.package_table.get(package_id)
            package.update_delivery_status(status)
 
    def get_nearest_package(self):

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

        return closest_package
    

    def deliver_package(self, min_distance, closest_package):
        time_to_travel = min_distance / self.speed * 60 #calculate time to travel to closest package
        self.time += timedelta(minutes=time_to_travel) #update truck time
        self.dispatcher.delivered_package_ids.append(closest_package.get_id()) #push package to delivered packages from the dispatcher
        self.delivered_package_ids.append(closest_package.get_id())
        self.last_package_delivered = closest_package.get_id() #update last package delivered
        self.miles += min_distance #update truck miles
        self.current_loc_index = closest_package.dist_matrix_index #update truck location index
        self.queued_package_ids.remove(closest_package.get_id()) #pop closest package off the truck queue
        closest_package.set_delivery_time(self.time) #update package delivery time
        closest_package.set_status("Delivered") #update package delivery status


    #deliver packages
    def move_truck(self):

        #if there are no more packagaes to deliver in the queue
        if len(self.queued_package_ids) == 0: 

            #if not at hub, go back to hub
            if self.current_loc_index != 0:
                self.return_to_hub(); 

            return

        closest_package = self.get_nearest_package()

        min_distance = self.dispatcher.distance_matrix[self.current_loc_index][closest_package.dist_matrix_index]

        minutes = min_distance / self.speed * 60

        delivery_eta = self.time + timedelta(minutes=(minutes))

        #this is to prevent the truck from moving faster than the live time 
        if delivery_eta >= self.dispatcher.live_time + timedelta(minutes=1):

            #update truck status
            eta = delivery_eta.strftime("%I:%M %p")
            self.status = f"En Route to " + str(closest_package.get_address()) + " (ETA: " + eta + ") "

            #print("Truck #" + str(self.truck_id) + " is " + self.status + "\n")

            return
        
        print(f"({self.dispatcher.live_time.strftime('%I:%M%p')}) (Delivered) Truck #{self.truck_id} | Location: {closest_package.get_address()} (ID: {closest_package.get_id()}) | Distance Traveled: {min_distance} | Total Miles: {self.miles + min_distance}")

        self.deliver_package(min_distance, closest_package)

        #step again, if there are more packages to deliver at the same time
        self.move_truck()
            

        

        