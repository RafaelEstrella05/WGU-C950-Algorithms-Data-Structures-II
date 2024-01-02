'''
This file is the main file for the dispatcher. It will be the object that is invoked by the main program so that 
it can dispatch the trucks and track the time. The dispatcher will be in charge of creating efficient routes for the 
trucks to take. It will also be in charge of updating routes and times as the trucks deliver packages.

Attributes:
- trucks: A structure of available trucks that have to be assigned to drivers
- drivers: A structure of available drivers that will be assigned to trucks
- packages: A structure of packages that will be delivered
    - packages are loaded from the packages.xlxs file and are stored in a graph based on the distances.xlsx file
- time: The current time of the dispatcher
- 
'''

# Constructor
class Dispatcher:

    #graph of distances between locations
    distance_graph = {}

    #attributes
    trucks = [] #list of trucks that are available
    drivers = [] #list of available drivers
    packages = [] #list of packages that need to be delivered (order them by deadline where EOD is last)
    assigned_trucks = [] #List of trucks that have been assigned to drivers and about to leave or have left
    step_count = 0 #current time of dispatcher in its own unit of time. is used to simulate 24 hour clock

    def assign_driver_to_truck(self, driver, truck):
        truck.driver = driver
        self.assigned_trucks.append(truck)

    #update_time
    def update_time(self, time):
        self.time = time

    #load distance graph node 
    def load_graph_node(self, location, destination, distance):
        if location not in self.distance_graph:
            self.distance_graph[location] = {}
        self.distance_graph[location][destination] = distance;

    # load package into dispatcher
    def load_package(self, package):
        if package.details["delivery_deadline"] == "EOD":
            self.packages.append(package)
        else:
            inserted = False
            for i in range(len(self.packages)):
                if package.is_deadline_before(self.packages[i]):
                    self.packages.insert(i, package)
                    inserted = True
                    break
            if not inserted:
                self.packages.append(package)
    

    #print distance graph
    def print_distance_graph(self):
        for location in self.distance_graph:
            for destination in self.distance_graph[location]:
                print(f"{location} -> {destination}: {self.distance_graph[location][destination]}")


    #print information about dispatcher
    def print_info(self):
        print("Trucks:")
        for truck in self.trucks:
            print(truck)

        print("Drivers:")
        for driver in self.drivers:
            print(driver)

        print("Packages:")
        for package in self.packages:
            package.print_delayed_arrival_time();
            print(package)

 


    