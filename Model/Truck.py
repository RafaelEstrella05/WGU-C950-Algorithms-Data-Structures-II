#Truck class


class Truck:
    
    #init
    def __init__(self, truck_id, driver, packages=None):
        self.truck_id = truck_id
        self.driver = driver
        self.assigned_packages = packages
        self.miles = 0
        self.route = []
        self.current_location = "HUB"
        self.speed = 18