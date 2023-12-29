import tkinter as tk
import time
#Import the Dispatcher, Truck, Driver, and Package classes that you've defined earlier
from Dispatcher import Dispatcher


class App:
    def __init__(self, root):
        self.root = root
        self.dispatcher = Dispatcher()  # Create a dispatcher instance
        self.elapsed_time = 0  # Time in seconds
        self.timer_speed = 1  # Speed can be adjusted to make time go faster or slower
        self.is_running = False  # Flag to track if the timer is running
        self.label = tk.Label(root, text="00:00:00", font=('Helvetica', 48))
        self.label.pack()
        self.update_clock()

        self.start_button = tk.Button(root, text="Start", command=self.toggle_timer)
        self.start_button.pack()


    def update_clock(self):
        if self.is_running:
            hours = self.elapsed_time // 3600
            minutes = (self.elapsed_time % 3600) // 60
            seconds = (self.elapsed_time % 3600) % 60
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.label.configure(text=time_str)
            self.elapsed_time += 1

            # Update the dispatcher's time here (if you're simulating time within the dispatcher)
            self.dispatcher.update_time(self.elapsed_time)

            print(self.dispatcher.time)  # Example of printing the dispatcher's time

        # Adjust the delay based on the timer speed
        self.root.after(1000 // self.timer_speed, self.update_clock)

    def toggle_timer(self):
        if self.is_running:
            self.start_button.configure(text="Start")
            self.is_running = False
        else:
            self.start_button.configure(text="Stop")
            self.is_running = True
            self.elapsed_time = 0

    def load_dispatcher_data(self):
        # Load trucks, drivers, packages, etc., into the dispatcher
        # Example: self.dispatcher.load_packages([...])
        pass

    def start_dispatch(self):
        # Start the dispatch process
        # This might include assigning drivers to trucks, creating routes, etc.
        # Example: self.dispatcher.dispatch_trucks()
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("WGUPS Delivery Timer")
    app = App(root)
    root.mainloop()
