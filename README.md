# WGUPS Package Delivery Simulation

## Overview

This project simulates a real-time package delivery system for Western Governors University Parcel Service (WGUPS) using the **Nearest Neighbor Algorithm**. It was developed as part of the **C950: Data Structures and Algorithms II** course at Western Governors University.

The program dynamically manages package deliveries across multiple trucks and drivers, accounting for constraints such as delayed packages and wrong addresses, all while minimizing mileage. A GUI interface and a headless mode are provided to visualize or simulate the process.

---

## Features

- 🚚 **Multiple Truck Management** with dynamic driver assignment  
- 🬝 **Greedy Nearest Neighbor Algorithm** for route optimization  
- 🕒 **Real-time Clock Simulation** starting at 8:00 AM  
- 💃 **Custom Hash Table** with resizing for package lookups (O(1) time complexity)  
- 📦 **Support for Delayed Packages** and incorrect addresses  
- 🖥️ **Interactive GUI** built with `tkinter`  
- 🔄 **Step-by-step simulation controls** (manual or automatic speed)  
- 🧪 **Headless mode** for command-line testing

---

## File Structure

```
.
├── main.py               # GUI application for live simulation
├── headless.py           # Console-based simulation for quick testing
├── Model/
│   ├── Dispatcher.py     # Controls trucks, drivers, and dispatch logic
│   ├── Truck.py          # Truck behavior and movement logic
│   ├── Driver.py         # Driver data model
│   ├── Package.py        # Package object model
│   ├── HashTable.py      # Custom hash table implementation
│   ├── Utils.py          # CSV loading utilities for distances and packages
├── Data/
│   ├── distances.csv     # Symmetric distance matrix
│   ├── packages.csv      # Package list with delivery deadlines and special notes
├── Task 2 Writing.pdf    # Design and algorithm justification (WGU submission)
```

---

## How It Works

- Packages are loaded into a **Hash Table** from `packages.csv`.
- Trucks are initialized with pre-assigned packages.
- Each truck uses the **Nearest Neighbor Algorithm** to determine its next delivery.
- Special delivery constraints (delays, wrong addresses) are automatically handled.
- Drivers can dynamically switch trucks to optimize delivery timing.

---

## Requirements

- Python 3.8+
- `tkinter` (pre-installed with most Python distributions)

---

## Running the Simulation

### Option 1: GUI Mode

Launch the interactive delivery simulator:

```bash
python main.py
```

Features:
- Pause, resume, and step-through simulation
- Visual tracking of each truck’s location, miles traveled, and packages delivered
- Color-coded statuses (Queued, Delivered, Delayed)

### Option 2: Headless Mode

Run the simulation in the terminal:

```bash
python headless.py
```

Displays live truck activity and prints all package statuses until delivery is complete.

---

## Algorithm Justification

This project uses a **greedy nearest neighbor algorithm** due to its simplicity and efficiency. It was chosen over alternatives like **Genetic Algorithms** or **Simulated Annealing** due to time constraints and project scope. Full justification and comparison of algorithms are included in `Task 2 Writing.pdf`.

---

## Potential Improvements

- 🔀 Dynamic clustering of delivery addresses (e.g., K-Medoids) to reduce mileage
- 📊 Advanced analytics dashboard (total mileage, on-time percentage)
- 🧠 Implementing smarter truck-to-package assignment for future scalability

---

## Author

**Rafael Estrella**  
WGU Student ID: 009970725  
Course: C950 – Data Structures and Algorithms II  
Instructor: Dr. Amy Antonucci

---


