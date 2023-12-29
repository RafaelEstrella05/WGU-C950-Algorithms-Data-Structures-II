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
            "delivery_status": "at hub",  # Initial status
        }

    def update_delivery_status(self, status):
        self.details["delivery_status"] = status

    def __str__(self):
        return f"Package ID: {self.details['package_id']}, Address: {self.details['address']}, Deadline: {self.details['delivery_deadline']}, Status: {self.details['delivery_status']}"

    #updates address only, ideal for address change within the same city
    def update_local_address(self, address):
        self.details["address"] = address

    #updates address, city, state, and zip code, ideal for address change to a different city
    def update_address(self, address, city, state, zip_code):
        self.details["address"] = address
        self.details["city"] = city
        self.details["state"] = state
        self.details["zip_code"] = zip_code

    