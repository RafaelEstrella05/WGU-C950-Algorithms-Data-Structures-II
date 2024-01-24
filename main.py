# Student ID: 009970725
# Author: Rafael Estrella

import tkinter as tk
from tkinter import ttk
from Model.Dispatcher import Dispatcher
from Model.Utils import load_distance_matrix, load_package_data
from datetime import datetime

global status_labels

pause = True
step_speed_index = 0
step_speeds = [2000, 1000, 500, 100, 50]

# Create dispatcher object for managing trucks and packages
dispatcher = Dispatcher()

# Load the distance matrix and package data into the dispatcher
load_distance_matrix(dispatcher)
load_package_data(dispatcher)

dispatcher.de_queue_unready_packages()

#handles simulation start and pause
def action_play():
    global action_button
    global pause

    if pause:
        pause = False
        action_button.config(text="Pause")

        #disable step button
        step_button.config(state="disabled")

        dispatch_step()
    else:
        pause = True
        action_button.config(text="Resume")

        #enable step button
        step_button.config(state="normal")


#carousels through speeds in the simulation
def change_speed():
    
    global step_speed_index
    global step_speeds
    global speed_button

    step_speed_index += 1
    if step_speed_index >= len(step_speeds):
        step_speed_index = 0

    speed_button.config(text=f"Speed: {step_speed_index + 1}")
    

#step through the dispatching one step at a time.
def manual_dispatch_step():

    if not dispatcher.is_dispatch_complete():
        dispatcher.dispatchStep()
        update_gui()
    else:
        action_button.config(text="Dispatch Complete")
        action_button.config(state="disabled")

def dispatch_step():

    if pause:
        return

    if not dispatcher.is_dispatch_complete():
        dispatcher.dispatchStep()
        #init_gui(dispatcher)
        update_gui()
        
        root.after(step_speeds[step_speed_index], dispatch_step)
    else:
        action_button.config(text="Dispatch Complete")
        action_button.config(state="disabled")

#initialize the gui and global gui components that will be used to update the gui
def init_gui(dispatcher):
    global status_labels, live_time_label, list_box_list, action_button, packages_label_list, step_button, speed_button, list_names, frames, listboxes
    status_labels = []
    list_box_list = [] #array of listboxes, one for each truck and each list
    packages_label_list = []

    # Clear the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Navigation bar frame at the top of the window
    nav_frame = tk.Frame(root, height=50)
    nav_frame.pack(side="top", fill="x", expand=False)

    #speed button on the right side of the navigation bar
    speed_button = tk.Button(nav_frame, text=f"Speed: {step_speed_index + 1}", command=change_speed)
    speed_button.pack(side="right", padx=10, pady=10, ipadx=10, ipady=10)
    
    #action button toggles between pause and resume
    action_button = tk.Button(nav_frame, text="Run", command=action_play)
    action_button.pack(side="right", padx=10, pady=10, ipadx=10, ipady=10)

    step_button = tk.Button(nav_frame, text="Step", command=manual_dispatch_step)
    step_button.pack(side="right", padx=10, pady=10, ipadx=10, ipady=10)

    # label for live time of dispatcher
    live_time_label = tk.Label(nav_frame, text=f"{dispatcher.live_time.strftime('%I:%M%p')}", anchor="center", justify="center", font=("Arial", 30))
    live_time_label.pack(side="top", fill="x", expand=True)

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

        #create status label
        truck_info = f"Truck: {truck.truck_id}\nMiles: {miles}\nDriver: {driver_text} \nLocation: {truck_location}\nLast Reported: {truck.time.strftime('%I:%M%p')}"
        status_label = tk.Label(status_frame, text=truck_info, bg="white", anchor="w", justify="left")
        status_label.pack(side="left", fill="x", expand=True)

        status_labels.append(status_label)

        #if truck has no more queued packages, and no more delayed packages, and is at the hub, then it is done
        if len(truck.queued_package_ids) == 0 and len(truck.delayed_package_ids) == 0 and truck.current_loc_index == 0:
            status_label.config(bg="#CCFFCC") #color light green if done


        # Packages list sections
        list_names = ['Queued', 'Delivered', 'Delayed']  # List to store the names of the lists
        frames = []  # List to store the frames for each package list
        listboxes = []  # List to store the listboxes

        # Create the frames and listboxes for each list
        for list_name in list_names:
            package_ids = getattr(truck, f'{list_name.lower()}_package_ids')

            if list_name == 'Queued':
                # Sort the queued packages by distance from the current location
                package_ids = sorted(package_ids, key=lambda pid: dispatcher.distance_matrix[truck.current_loc_index][dispatcher.package_table.get(pid).dist_matrix_index])
            if list_name == 'Delivered':
                # Sort the delivered packages by delivery time
                package_ids = sorted(package_ids, key=lambda pid: dispatcher.package_table.get(pid).get_delivery_time(), reverse=True)

            # Frame for the list
            frame = tk.Frame(truck_frame, background="#DDDDDD")
            frame.pack(fill="both", expand=True)
            if list_name == 'Delayed':
                frame.config(height=100)
                frame.pack_propagate(False)

            packages_label = tk.Label(frame, text=f"{list_name} Packages ({len(package_ids)})", bg="#DDDDDD")
            packages_label.pack(side="top", fill="x")

            packages_label_list.append(packages_label)


            # Listbox for the packages
            listbox = tk.Listbox(frame)
            listbox.pack(side="left", fill="both", expand=True)

            #make fixed width
            listbox.config(width=50)

            list_box_list.append(listbox)

            # Populate listbox with package information
            for package_id in package_ids:
                package = dispatcher.package_table.get(package_id)
                if package:
                    package_info = f"ID: {package.get_id()} | at {package.address}"
                    if package.delivery_deadline != "EOD":
                        package_info += f" | Deadline: {package.delivery_deadline}"
                    
                    if list_name == 'Delivered':
                        delivery_time = package.get_delivery_time().strftime('%I:%M%p')
                        package_info += f" | Delivered: {delivery_time} "
                        listbox.insert("end", package_info)
                        listbox.itemconfig("end", {'bg':'#CCFFCC'})  # Color light green if delivered on time
                    elif list_name == 'Delayed':
                        distance_from_current_location = dispatcher.distance_matrix[truck.current_loc_index][package.dist_matrix_index]
                        distance_from_current_location = round(distance_from_current_location, 1)
                        delayed_reason = ""
                        if package.delayed_address is not None:
                            delayed_reason = " (wrong address)"
                        else:
                            delayed_reason = " (delayed: arriving to hub: " + package.delayed_arrival_time.strftime('%I:%M%p') + ")"
                        package_info += f" | {distance_from_current_location} miles away {delayed_reason}"
                        listbox.insert("end", package_info)
                        listbox.itemconfig("end", {'bg':'#FFCC99'})  # Color light orange if delayed
                    else:
                        distance_from_current_location = dispatcher.distance_matrix[truck.current_loc_index][package.dist_matrix_index]
                        distance_from_current_location = round(distance_from_current_location, 1)
                        package_info += f" | {distance_from_current_location} miles away"
                        listbox.insert("end", package_info)

            

            # Scrollbar for the listbox
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
            scrollbar.pack(side="right", fill="y")
            listbox.config(yscrollcommand=scrollbar.set)

            if list_name == 'Queued' and len(package_ids) > 0:
                listbox.itemconfig(0, {'bg':'#FFFFCC'}) #color light yellow if queued

            # Append the created frame and listbox to their respective lists
            frames.append(frame)
            listboxes.append(listbox)

def update_gui():
    global status_labels, live_time_label, list_box_list, action_button, speed_button, step_button
    
    #update the live time label
    live_time_label.config(text=f"{dispatcher.live_time.strftime('%I:%M%p')}")
    
    #nav button update
    if dispatcher.is_dispatch_complete():

        #disable step button
        step_button.config(state="disabled")

        #disable speed button
        speed_button.config(state="disabled")

    #for every truck
    for i, truck in enumerate(dispatcher.trucks):
        
        #update the status label
        driver_text = "None"
        if truck.driver_index is not None:
            driver_text = f"Driver {int(truck.driver_index) + 1}"
        truck_location = dispatcher.location_labels[truck.current_loc_index]
        if truck.current_loc_index == 0:
            truck_location = "HUB"
        miles = round(truck.miles, 1);
        truck_info = f"Truck: {truck.truck_id}\nMiles: {miles}\nDriver: {driver_text} \nLast Reported Location: {truck_location}\nLast Reported Time: {truck.time.strftime('%I:%M%p')}\nStatus: {truck.status}"
        status_labels[i].config(text=truck_info)

        #if truck has no more queued packages, and no more delayed packages, and is at the hub, then it is done
        if len(truck.queued_package_ids) == 0 and len(truck.delayed_package_ids) == 0 and truck.current_loc_index == 0:
            status_labels[i].config(bg="#CCFFCC")

        truck_packages_lists = [truck.queued_package_ids, truck.delivered_package_ids, truck.delayed_package_ids]

        list_names = ['Queued', 'Delivered', 'Delayed']  # List to store the names of the lists

        #for each list of packages in the truck
        for j, truck_packages_list in enumerate(truck_packages_lists):
            #update the listbox
            listbox = list_box_list[i*3 + j]
            listbox.delete(0, "end")

            #if list is delivered
            if j == 1:
                #sort the delivered packages by delivery time from latest to earliest
                truck_packages_list = sorted(truck_packages_list, key=lambda pid: dispatcher.package_table.get(pid).get_delivery_time(), reverse=True)

            #if list is queued
            if j == 0:
                #sort the queued packages by distance from the current location
                truck_packages_list = sorted(truck_packages_list, key=lambda pid: dispatcher.distance_matrix[truck.current_loc_index][dispatcher.package_table.get(pid).dist_matrix_index])

            #update package label
            packages_label_list[i*3 + j].config(text=f"{list_names[j]} Packages ({len(truck_packages_list)})")

            #for every package in the truck_pacakges_list
            for package_id in truck_packages_list:
                package = dispatcher.package_table.get(package_id)
                
                if package:
                    package_info = f"ID: {package.get_id()} | at {package.address}"
                    if package.delivery_deadline != "EOD":
                        package_info += f" | Deadline: {package.delivery_deadline}"
                    
                    if j == 1: #if list is delivered
                        delivery_time = package.get_delivery_time().strftime('%I:%M%p')
                        package_info += f" | Delivered: {delivery_time} "
                        listbox.insert("end", package_info)
                        listbox.itemconfig("end", {'bg':'#CCFFCC'})  # Color light green if delivered on time
                    elif j == 2: #if list is delayed
                        distance_from_current_location = dispatcher.distance_matrix[truck.current_loc_index][package.dist_matrix_index]
                        distance_from_current_location = round(distance_from_current_location, 1)

                        delayed_reason = ""
                        if package.delayed_address is not None:
                            delayed_reason = " (wrong address)"
                        else:
                            delayed_reason = " Delayed: arriving to the hub at " + package.delayed_arrival_time.strftime('%I:%M%p')
                        package_info += f" | {delayed_reason}"


                        listbox.insert("end", package_info)
                        listbox.itemconfig("end", {'bg':'#FFCC99'})  # Color light orange if delayed
                    else: #if list is queued
                        distance_from_current_location = dispatcher.distance_matrix[truck.current_loc_index][package.dist_matrix_index]
                        distance_from_current_location = round(distance_from_current_location, 1)
                        package_info += f" | {distance_from_current_location} miles away"
                        listbox.insert("end", package_info)

                        #color the first queued package light yellow
                        if j == 0 and package_id == truck_packages_list[0]:
                            listbox.itemconfig("end", {'bg':'#FFFFCC'})




# Main application window
root = tk.Tk()
root.title("WGU C950 Package Delivery")

#make screen as large as possible
root.state('zoomed')

# Initial GUI setup
init_gui(dispatcher)

# Run the application
root.mainloop()
