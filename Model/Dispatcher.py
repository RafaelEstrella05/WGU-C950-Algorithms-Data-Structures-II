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
    trucks = []
    drivers = []
    packages = []
    assigned_trucks = []

    #update_time
    def update_time(self, time):
        self.time = time

    #load distance graph node 
    def load_graph_node(self, location, destination, distance):
        if location not in self.distance_graph:
            self.distance_graph[location] = {}
        self.distance_graph[location][destination] = distance;
        



    