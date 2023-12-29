# controllers/controller.py
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_model(self, data):
        self.model.set_data(data)
        self.update_view()

    def update_view(self):
        data = self.model.get_data()
        self.view.update_view(data)
