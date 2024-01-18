import tkinter as tk

# Initialize the main window
root = tk.Tk()
root.title("Truck Status Dashboard")

#geometry should be full screen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))



root.mainloop()