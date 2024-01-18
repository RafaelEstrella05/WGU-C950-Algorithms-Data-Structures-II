from datetime import datetime
class Package:
    def __init__(self, dispatcher, package_id, address, city, state, zip_code, delivery_deadline, weight_kilo, special_notes=None):
        
        self.package_id = int(package_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight_kilo = weight_kilo
        self.special_notes = special_notes
        self.delivered_time = None #time that package was delivered
        self.status = "At Hub"

        self.dispatcher = dispatcher #dispatcher object (parent)

        self.set_matrix_index() #index of the location in the distance matrix (used for calculating distance traveled)

        self.delayed_arrival_time = None #time that package will arrive at destination if delayed
        self.delayed_address_time = None
        self.delayed_address = None

        #if special note is "Delayed on flight---will not arrive to depot until XX:XX PM"
        if self.special_notes is not None:
            if "Delayed on flight" in special_notes.lower():
                time = special_notes.split("until ")[1]
                self.delayed_arrival_time = datetime.strptime(time, "%I:%M %p").time()

            #if special note is "Wrong address listed" find the correct address example: "Wrong address listed: new address known at 10:20 a.m (410 S. State St., Salt Lake City, UT 84111)"
            if "wrong address" in special_notes.lower():
                #time
                time = special_notes.split("known at ")[1].split(" ")[0]
                time = datetime.strptime(time, "%I:%M").time()
                self.delayed_address_time = time

                #address with, state, and zip code
                address = special_notes.split("\"")[1].split("\"")[0] #410 S. State St 84111
                self.delayed_address = address

    def get_id(self):
        
        return self.package_id
    
    def get_address(self):
        
        return self.address 
    
    def set_address(self, address):
        
        self.address = address

    #used for easy distance matrix lookup
    def set_matrix_index(self):

        package_address = self.address + " (" + self.zip_code + ")"
        self.dist_matrix_index = self.dispatcher.get_location_index(package_address)

        if(self.dist_matrix_index == None):
             #"Error could not find distance matrix for package id: X"
             print("Error could not find distance matrix for package id: " + str(self.package_id))

    def set_delayed_matrix_index(self):

        self.dist_matrix_index = self.dispatcher.get_location_index(self.delayed_address)
        

    def get_zip_code(self):
            
            return self.zip_code

    def set_status(self, status):
        
        self.status = status

    def get_status(self):
            
            return self.status

    

    def set_delivery_time(self, datetime):
        self.delivered_time = datetime
        

    def update_delivery_status(self, status):
        
        self.delivery_status = status

    def get_matrix_index():
        pass

    #updates address only, ideal for address change within the same city
    def update_local_address(self, address):
        
        self.address = address

    #updates address, city, state, and zip code, ideal for address change to a different city
    def update_address(self, address, city, state, zip_code):
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code


    
    def print_delayed_arrival_time(self):
        if self.delayed_arrival_time is not None:
            print(f"Package {self.package_id} is delayed and will arrive at {self.delayed_arrival_time.strftime('%I:%M %p')}")
        else:
            print(f"Package {self.package_id} is not delayed")
    
    def __str__(self):
        return f"Package ID: {self.package_id}, Address: {self.address}, Deadline: {self.delivery_deadline}, Status: {self.get_status()}, Special Notes: {self.special_notes}"
        
        

