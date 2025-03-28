from Model.Package import Package

class HashTable:
    def __init__(self, size=57):
        self.size = size
        self.count = 0
        self.table = [[] for _ in range(size)]
        # Constant for multiplication method : reciprocal of golden ratio = (sqrt(5) - 1) / 2), used for avoiding collisions 
        self.A = 0.6180339887498949  

    def hash_function(self, key):
        hash_value = int(self.size * ((key * self.A) % 1)) #multiplication method
        return hash_value

    def check_load_and_resize(self):
        load_factor = self.count / self.size
        if load_factor > 0.7:
            self.resize()

    def resize(self):
        self.size *= 2
        old_table = self.table
        self.table = [[] for _ in range(self.size)]
        self.count = 0

        for bucket in old_table:
            for package in bucket:
                self.insert(package)

    def insert(self, package):
        #verify that package is a Package object
        if not isinstance(package, Package):
            print("ERROR: Item cannot be inserted into Hash Table: not a Package object")
            return
        self.check_load_and_resize()
        
        hash_key = self.hash_function(package.get_id())
        bucket = self.table[hash_key]

        for i, existing_package in enumerate(bucket):
            if existing_package.get_id() == package.get_id():
                # Replace existing package with the same ID
                bucket[i] = package
                return

        # If no existing package with the same ID, append the new package
        bucket.append(package)
        self.count += 1

    def get(self, package_id):
        #verify that package_id is an int
        if not isinstance(package_id, int):
            print("ERROR: Item cannot be retrieved from Hash Table: argument not an int")
            return None

        hash_key = self.hash_function(package_id)
        for package in self.table[hash_key]:
            if package.get_id() == package_id:
                return package
        return None

    def display(self):
        for index, bucket in enumerate(self.table):
            if bucket:
                print(f"Bucket {index}: {[package.get_id() for package in bucket]}")


