
class Driver:
    def __init__(self, driver_id, name, truck):
        self.driver_id = driver_id
        self.name = name
        self.truck = truck

    def get_id(self):
        return self.driver_id

    def get_name(self):
        return self.name

    def get_truck(self):
        return self.truck

    def set_truck(self, truck):
        self.truck = truck

    def remove_truck(self):
        self.truck = None