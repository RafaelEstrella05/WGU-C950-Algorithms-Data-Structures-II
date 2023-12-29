# views/view.py
import tkinter as tk

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Example Label
        self.label = tk.Label(self, text="Hello MVC!")
        self.label.pack()

        # Example Entry
        self.entry = tk.Entry(self)
        self.entry.pack()

        # Example Button
        self.button = tk.Button(self, text="Update Model", command=self.update_model)
        self.button.pack()

    def update_model(self):
        data = self.entry.get()
        self.controller.update_model(data)

    def update_view(self, data):
        self.label.config(text=data)
