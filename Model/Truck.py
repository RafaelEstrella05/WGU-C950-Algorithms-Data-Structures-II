#Truck class

class Truck:
    
    #init
    def __init__(self, truck_id, driver, packages=None):
        self.truck_id = truck_id
        self.driver = driver #driver object
        self.assigned_packages = packages #list of package objects currently assigned to truck
        self.miles = 0 
        self.route = []
        self.current_location = "HUB"
        self.speed = 18