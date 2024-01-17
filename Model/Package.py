from datetime import datetime
class Package:
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight_kilo, special_notes=None):
        self.details = {
            "package_id": package_id,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "delivery_deadline": delivery_deadline, #Example: "10:30 AM", "EOD"
            "weight_kilo": weight_kilo,
            "special_notes": special_notes,
            "delivery_status": "at hub",  # Initial status (at hub, en route, delivered)
            "assigned_truck_id": None,  # Truck object
        }

        #convert package_id to int
        self.details["package_id"] = int(self.details["package_id"])

        self.dist_matrix_index = None #index of the location in the distance matrix (used for calculating distance traveled)


        self.delayed_arrival_time = None #time that package will arrive at destination if delayed

        self.delayed_address_time = None
        self.delayed_address = None

        self.delivered_time = None #time that package was delivered

        #if special note is "Delayed on flight---will not arrive to depot until XX:XX PM"
        if special_notes is not None:
            if "Delayed on flight" in special_notes.lower():
                time = special_notes.split("until ")[1]
                self.delayed_arrival_time = datetime.strptime(time, "%I:%M %p").time()

            #if special note is "Wrong address listed" find the correct address example: "Wrong address listed: new address known at 10:20 a.m (410 S. State St., Salt Lake City, UT 84111)"
            if "wrong address" in special_notes.lower():
                #time
                time = special_notes.split("known at ")[1].split(" ")[0]
                time = datetime.strptime(time, "%I:%M").time()
                self.delayed_address_time = time

                #address
                address = special_notes.split("(")[1].split(")")[0]
                self.delayed_address = address

    def get_id(self):
        return self.details["package_id"]
    
    def get_address(self):
        return self.details["address"]
    
    def set_address(self, address):
        self.details["address"] = address

    def set_delivery_status(self, status):
        self.details["delivery_status"] = status

    def set_delivery_time(self, datetime):
        self.delivered_time = datetime
        

    def update_delivery_status(self, status):
        self.details["delivery_status"] = status


    #updates address only, ideal for address change within the same city
    def update_local_address(self, address):
        self.details["address"] = address

    #updates address, city, state, and zip code, ideal for address change to a different city
    def update_address(self, address, city, state, zip_code):
        self.details["address"] = address
        self.details["city"] = city
        self.details["state"] = state
        self.details["zip_code"] = zip_code
    
    def get_id(self):
        return self.details["package_id"]

    #method to find if one deadline is before another.
    def is_deadline_before(self, other_package):
        if self.details["delivery_deadline"] == "EOD":
            return False
        elif other_package.details["delivery_deadline"] == "EOD":
            return True
        else:
            self_deadline = self.details["delivery_deadline"]
            other_deadline = other_package.details["delivery_deadline"]

            if self_deadline == other_deadline:
                return False 

            if self_deadline == "EOD":
                return False
            elif other_deadline == "EOD":
                return True

            self_time = datetime.strptime(self_deadline, "%I:%M %p").time()
            other_time = datetime.strptime(other_deadline, "%I:%M %p").time()

            return self_time < other_time
    
    def print_delayed_arrival_time(self):
        if self.delayed_arrival_time is not None:
            print(f"Package {self.details['package_id']} is delayed and will arrive at {self.delayed_arrival_time.strftime('%I:%M %p')}")
        else:
            print(f"Package {self.details['package_id']} is not delayed")
    
    def __str__(self):
        return f"Package ID: {self.details['package_id']}, Address: {self.details['address']}, Deadline: {self.details['delivery_deadline']}, Status: {self.details['delivery_status']}, Special Notes: {self.details['special_notes']}"
        
        

'''
#Test Script
        
#Create test packages
test_packages = []
test_packages.append(Package(1, "123 Test Address", "Test City", "Test State", "12345", "10:30 AM", 10))
test_packages.append(Package(2, "123 Test Address", "Test City", "Test State", "12345", "EOD", 10))
test_packages.append(Package(8, "123 Test Address", "Test City", "Test State", "12345", "2:30 PM", 10))
test_packages.append(Package(3, "123 Test Address", "Test City", "Test State", "12345", "9:00 AM", 10))
test_packages.append(Package(4, "123 Test Address", "Test City", "Test State", "12345", "EOD", 10))
test_packages.append(Package(5, "123 Test Address", "Test City", "Test State", "12345", "12:00 AM", 10))
test_packages.append(Package(6, "123 Test Address", "Test City", "Test State", "12345", "EOD", 10))
test_packages.append(Package(7, "123 Test Address", "Test City", "Test State", "12345", "2:00 PM", 10))


#Test deadline sorting
sorted_packages = []

for package in test_packages:
    inserted = False
    for i in range(len(sorted_packages)):
        if package.is_deadline_before(sorted_packages[i]):
            sorted_packages.insert(i, package)
            inserted = True
            break
    if not inserted:
        sorted_packages.append(package)

for package in sorted_packages:
    print(package)


'''
