import tkinter as tk

# Initialize the main window
root = tk.Tk()
root.title("Truck Status Dashboard")
root.geometry("900x300")

# Define data for the trucks (as an example, this could come from a database or other data source)
trucks_data = [
    {'id': 1, 'distance': '30 miles', 'last_address': '123 Main St', 'status': 'In Route', 'deliveries': [
        ('35', 'Delivered'), ('4', 'In Route'), ('6', 'In Route'), ('10', 'In Route'), ('7', 'In Route'), ('27', 'In Route'),  ('1', 'In Route'), ('40', 'In Route'),
        ('29', 'In Route'), ('15', 'In Route'), ('13', 'In Route'), ('30', 'In Route'), ('20', 'In Route'), ('37', 'In Route'), ('14', 'In Route'), ('16', 'In Route'),
        ('34', 'In Route'), ('18', 'In Route'), ('19', 'In Route'), ('39', 'In Route'), ('36', 'In Route'), ('3', 'In Route'), ('8', 'In Route'), ('9', 'In Route'),
        ('38', 'In Route')
    ]},
    {'id': 2, 'distance': '30 miles', 'last_address': '456 Oak St', 'status': 'Delayed', 'deliveries': [
        ('35', 'Delivered'), ('4', 'In Route'), ('6', 'Delayed'), ('10', 'In Route'), ('7', 'In Route'), ('27', 'In Route'),  
        ('1', 'In Route'), ('40', 'In Route'), ('29', 'In Route'), ('15', 'In Route'), ('13', 'In Route'), ('30', 'In Route'),
        ('20', 'In Route'), ('37', 'In Route'), ('14', 'In Route'), ('16', 'In Route'), ('34', 'In Route'), ('18', 'In Route'),
        ('19', 'In Route'), ('39', 'In Route'), ('36', 'In Route'), ('3', 'In Route'), ('8', 'In Route'), ('9', 'In Route'),
        ('38', 'In Route')
    ]},
    {'id': 3, 'distance': '30 miles', 'last_address': '789 Pine St', 'status': 'At Hub', 'deliveries': [
        ('35', 'At Hub'), ('4', 'At Hub'), ('6', 'At Hub'), ('10', 'At Hub'), ('7', 'At Hub'), ('27', 'At Hub'),  
        ('1', 'At Hub'), ('40', 'At Hub'), ('29', 'At Hub'), ('15', 'At Hub'), ('13', 'At Hub'), ('30', 'At Hub'),
        ('20', 'At Hub'), ('37', 'At Hub'), ('14', 'At Hub'), ('16', 'At Hub'), ('34', 'At Hub'), ('18', 'At Hub'),
        ('19', 'At Hub'), ('39', 'At Hub'), ('36', 'At Hub'), ('3', 'At Hub'), ('8', 'At Hub'), ('9', 'At Hub'),
        ('38', 'At Hub')
    ]}
]

# Function to create a label dynamically
def create_label(master, text, bg_color):
    label = tk.Label(master, text=text, bg=bg_color)
    label.pack(pady=2, fill='x')

# Create truck frames and labels dynamically
for truck in trucks_data:
    # Create a frame for each truck
    truck_frame = tk.Frame(root, bg='lightgrey', bd=2, relief='groove')
    truck_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    # Create a title label for the truck
    create_label(truck_frame, f"Truck #{truck['id']}", 'lightblue')
    
    # Create labels for distance, last address, and status
    create_label(truck_frame, f"Total Distance: {truck['distance']}", 'lightgrey')
    create_label(truck_frame, f"Last Address: {truck['last_address']}", 'lightgrey')
    create_label(truck_frame, f"Status: {truck['status']}", 'lightgrey')
    
    # Create labels for each delivery item
    for delivery in truck['deliveries']:
        delivery_id, delivery_status = delivery
        color = 'green' if delivery_status == 'Delivered' else 'red' if delivery_status == 'Delayed' else 'lightgrey'
        create_label(truck_frame, f"#{delivery_id} {delivery_status}", color)

# Start the main GUI loop
root.mainloop()
