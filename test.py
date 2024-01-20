import tkinter as tk
from tkinter import ttk
from Model.Dispatcher import Dispatcher
from Model.Utils import load_distance_matrix, load_package_data

# Create dispatcher object
dispatcher = Dispatcher()
load_distance_matrix(dispatcher)
load_package_data(dispatcher)

# Function calls the dispatcher to move to the next truck step
def next_truck_step():
    if not dispatcher.is_dispatch_complete():
        dispatcher.dispatchStep()
        display_gui(dispatcher)

def display_gui(dispatcher):
    # Clear the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Navigation bar frame (red)
    nav_frame = tk.Frame(root, height=50)
    nav_frame.pack(side="top", fill="x", expand=False)

    # Button on the right side of the navigation bar
    nav_button = tk.Button(nav_frame, text="Next Truck Step", command=next_truck_step)
    nav_button.pack(side="right", padx=10)

    # Create frames for each truck
    for i, truck in enumerate(dispatcher.trucks):
        truck_frame = tk.Frame(root, borderwidth=2, relief="groove")
        truck_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Status section (yellow)
        status_frame = tk.Frame(truck_frame, background="yellow", height=100)
        status_frame.pack(fill="x", expand=False)

        driver_text = "None"
        if truck.driver_index is not None:
            driver_text = f"Driver {int(truck.driver_index) + 1}"
        
        # Truck information
        truck_info = f"Truck {truck.truck_id}: {truck.miles} Total Miles \nDriver {driver_text} \nCurrent Loc: {dispatcher.location_labels[truck.current_loc_index]}"
        status_label = tk.Label(status_frame, text=truck_info, bg="yellow", anchor="w", justify="left")
        status_label.pack(side="left", fill="x", expand=True)



        # Packages list sections
        list_frames = {}  # Dictionary to store the frames for each package list
        listboxes = {}  # Dictionary to store the listboxes
        for list_name, package_ids in [('Queued', truck.queued_package_ids),
                                       ('Delivered', truck.delivered_package_ids),
                                       ('Delayed', truck.delayed_package_ids)]:
            # Frame for the list
            list_frames[list_name] = tk.Frame(truck_frame, background="#DDDDDD")
            list_frames[list_name].pack(fill="both", expand=True) 
            packages_label = tk.Label(list_frames[list_name], text=f"{list_name} Packages", bg="#DDDDDD")
            packages_label.pack(side="top", fill="x")

            # Listbox for the packages
            listboxes[list_name] = tk.Listbox(list_frames[list_name])
            listboxes[list_name].pack(side="left", fill="both", expand=True)

            # Populate listbox with package information
            for package_id in package_ids:
                package = dispatcher.package_table.get(package_id)
                if package:
                    if list_name == 'Delivered':
                        # Show delivery time for delivered packages
                        delivery_time = package.get_delivery_time().strftime('%I:%M%p')
                        listboxes[list_name].insert("end", f"ID: {package.get_id()} | at {package.address} | {delivery_time} ")
                    else:
                        listboxes[list_name].insert("end", f"ID: {package.get_id()}, Address: {package.address}")

            # Scrollbar for the listbox
            scrollbar = ttk.Scrollbar(list_frames[list_name], orient="vertical", command=listboxes[list_name].yview)
            scrollbar.pack(side="right", fill="y")
            listboxes[list_name].config(yscrollcommand=scrollbar.set)

# Main application window
root = tk.Tk()
root.title("Truck and Package Management")

# Initial GUI setup
display_gui(dispatcher)

# Run the application
root.mainloop()
