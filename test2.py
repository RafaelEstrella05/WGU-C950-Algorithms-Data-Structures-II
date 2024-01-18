'''
Develop a hash table, without using any additional libraries or classes, that has an insertion function that takes the package ID as input and inserts each of the following data components into the hash table:

•   delivery address

•   delivery deadline

•   delivery city

•   delivery zip code

•   package weight

•   delivery status (i.e., at the hub, en route, or delivered), including the delivery time


B.  Develop a look-up function that takes the package ID as input and returns each of the following corresponding data components:

•   delivery address

•   delivery deadline

•   delivery city

•   delivery zip code

•   package weight

•   delivery status (i.e., at the hub, en route, or delivered), including the delivery time
'''

from Model.Dispatcher import Dispatcher
from Model.Utils import load_distance_matrix, load_package_data

# Hash table class using chaining.
class HashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
    
    # Inserts a new item into the hash table.
    def insert(self, item):
        # get the bucket list where this item will go.
        bucket = hash(item) % len(self.table)
        bucket_list = self.table[bucket]
    
        # insert the item to the end of the bucket list.
        bucket_list.append(item)
    
    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
    
        # search for the key in the bucket list
        for item in bucket_list:
            if item == key:
                # find the item's index and return the item that is in the bucket list.
                index = bucket_list.index(item)
                return bucket_list[index]
    
        # the key is not found.
        return None
    
    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
    
        # remove the item from the bucket list if it is present.
        if key in bucket_list:
            bucket_list.remove(key)
    
    # Overloaded string conversion method to create a string
    # representation of the entire hash table. Each bucket is shown
    # as a pointer to a list object.
    def __str__(self):
        index = 0
        s = "   --------\n"
        for bucket in self.table:
            s += "%2d:|   %s\n" % (index, bucket)
            index += 1
        s += "   --------"
        return s
    

#create dispatcher
dispatcher = Dispatcher()

#load distance matrix and package data
load_distance_matrix(dispatcher);
load_package_data(dispatcher);

#initialize drivers, trucks, truck drivers, and packages
dispatcher.initDrivers();
dispatcher.initTrucks();
dispatcher.initTruckDrivers();
dispatcher.initPackages();

#initialize hash table
hash_table = HashTable()

#for every package in each truck, insert the package into the hash table
for truck in dispatcher.trucks:
    for package in dispatcher.trucks[truck].queued_packages:
        hash_table.insert(package)

#search for package 9
package = hash_table.search(9)

#print package data
print(package)

#remove package 9
hash_table.remove(package)

#search for package 9 again
package = hash_table.search(9)

#print package data
print(package)

#search for package 14
package = hash_table.search(14)

#print package data
print(package)





