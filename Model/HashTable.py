class HashTable:
    def __init__(self, size=57):  # Default size based on load factor calculation
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, package):
        # Using package_id as the key for hashing
        hash_key = self.hash_function(package.get_id())
        # Append the package to the appropriate bucket
        self.table[hash_key].append(package)

    def get(self, package_id):
        hash_key = self.hash_function(package_id)
        for package in self.table[hash_key]:
            if package.get_id() == package_id:
                return package
        return None  # Package not found

    def display(self):  # Optional method for debugging
        for index, bucket in enumerate(self.table):
            if bucket:
                print(f"Bucket {index}: {[package.get_id() for package in bucket]}")
