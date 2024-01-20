import tkinter as tk
from tkinter import ttk
from Model.Dispatcher import Dispatcher
from Model.Utils import load_distance_matrix, load_package_data
from datetime import datetime


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
    nav_button = tk.Button(nav_frame, text="Next Step", command=next_truck_step)
    nav_button.pack(side="right", padx=10, pady=10, ipadx=10, ipady=10)
    #if the dispatch is complete, disable the button
    if dispatcher.is_dispatch_complete():
        nav_button.config(state="disabled")
        #change text to complete
        nav_button.config(text="Dispatch Complete")

    # Create frames for each truck
    for i, truck in enumerate(dispatcher.trucks):
        truck_frame = tk.Frame(root, borderwidth=2, relief="groove")
        truck_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Status section
        status_frame = tk.Frame(truck_frame, background="white", height=100)
        status_frame.pack(fill="x", expand=False)

        driver_text = "None"
        if truck.driver_index is not None:
            driver_text = f"Driver {int(truck.driver_index) + 1}"
        
        # Truck information
        truck_location = dispatcher.location_labels[truck.current_loc_index]
        if truck.current_loc_index == 0:
            truck_location = "HUB"
        #miles round to one decimal place
        miles = round(truck.miles, 1);

        truck_info = f"Truck: {truck.truck_id}\nMiles: {miles}\nDriver: {driver_text} \nLocation: {truck_location}\nLast Reported: {truck.time.strftime('%I:%M%p')}"
        status_label = tk.Label(status_frame, text=truck_info, bg="white", anchor="w", justify="left")
        status_label.pack(side="left", fill="x", expand=True)

        #if truck has no more queued packages, and no more delayed packages, and is at the hub, then it is done
        if len(truck.queued_package_ids) == 0 and len(truck.delayed_package_ids) == 0 and truck.current_loc_index == 0:
            status_label.config(bg="#CCFFCC")
            status_label.config(text=f"Truck: {truck.truck_id}\nMiles: {miles}\nDriver: {driver_text} \nLocation: {truck_location}\nLast Reported: {truck.time.strftime('%I:%M%p')}\nStatus: Done")



        # Packages list sections
        list_frames = {}  # Dictionary to store the frames for each package list
        listboxes = {}  # Dictionary to store the listboxes
        for list_name, package_ids in [('Queued', truck.queued_package_ids),
                                       ('Delivered', truck.delivered_package_ids),
                                       ('Delayed', truck.delayed_package_ids)]:
            
            if list_name == 'Queued':
                package_ids = sorted(package_ids, key=lambda pid: dispatcher.distance_matrix[truck.current_loc_index][dispatcher.package_table.get(pid).dist_matrix_index])
            # if delivered, sort by delivery time from greatest to least
            if list_name == 'Delivered':
                package_ids = sorted(package_ids, key=lambda pid: dispatcher.package_table.get(pid).get_delivery_time(), reverse=True)

            # Frame for the list
            list_frames[list_name] = tk.Frame(truck_frame, background="#DDDDDD")
            list_frames[list_name].pack(fill="both", expand=True) 

            #if frame is delayed, height should be less, keep padding
            if list_name == 'Delayed':
                list_frames[list_name].config(height=100)
                list_frames[list_name].pack_propagate(False)


            packages_label = tk.Label(list_frames[list_name], text=f"{list_name} Packages ({len(package_ids)})", bg="#DDDDDD")
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
                        if package.delivery_deadline != "EOD":
                            delivery_deadline = f" | Deadline: {package.delivery_deadline} "
                        else:
                            delivery_deadline = ""

                        listboxes[list_name].insert("end", f"ID: {package.get_id()} | at {package.address}{delivery_deadline} | Delivered: {delivery_time} ")

                        listboxes[list_name].itemconfig("end", {'bg':'#CCFFCC'}) #color light green if delivered on time
                        
                        if package.delivery_deadline != "EOD":
                            delivery_deadline = datetime.strptime(package.delivery_deadline, '%I:%M %p').time()
                            package_del_time = package.get_delivery_time().time()
                            if package_del_time >= delivery_deadline:
                                listboxes[list_name].itemconfig("end", {'bg':'#FFCCCC'}) #color light red if delayed

                        
                        
                    else:
                        if package.delivery_deadline != "EOD":
                            delivery_deadline = f" | Deadline: {package.delivery_deadline}"
                        else:
                            delivery_deadline = ""


                        distance_from_current_location = dispatcher.distance_matrix[truck.current_loc_index][package.dist_matrix_index]
    

                        listboxes[list_name].insert("end", f"ID: {package.get_id()} | at {package.address}{delivery_deadline} | {distance_from_current_location} miles away")
                        #color light orange if delayed
                        if list_name == 'Delayed':
                            listboxes[list_name].itemconfig("end", {'bg':'#FFCC99'})

            # Scrollbar for the listbox
            scrollbar = ttk.Scrollbar(list_frames[list_name], orient="vertical", command=listboxes[list_name].yview)
            scrollbar.pack(side="right", fill="y")
            listboxes[list_name].config(yscrollcommand=scrollbar.set)

            #color the first item in the list to light yellow
            if list_name == 'Queued' and len(package_ids) > 0:
                listboxes[list_name].itemconfig(0, {'bg':'#FFFFCC'})

# Main application window
root = tk.Tk()
root.title("Truck and Package Management")

#make screen as large as possible
root.state('zoomed')

# Initial GUI setup
display_gui(dispatcher)

# Run the application
root.mainloop()
