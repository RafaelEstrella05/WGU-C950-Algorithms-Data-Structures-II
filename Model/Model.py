# models/model.py
class Model:
    def __init__(self):
        self.data = "Initial Data"

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
