To start testing different algorithms for efficiency in the context of your project for the WGUPS Routing Program, you need to follow a systematic approach. Here's a step-by-step guide to help you get started:

A. Selection of Algorithm
Research Algorithms: Given the scenario, algorithms like the Nearest Neighbor Algorithm, Greedy Algorithm, or even more complex ones like Genetic Algorithms might be suitable. Understand their workings, strengths, and weaknesses.

Criteria for Selection: Define what makes an algorithm 'efficient' for your use case. Is it the shortest path, least time, or adaptability to changing conditions?

Initial Hypothesis: Form a hypothesis about which algorithm might work best based on your understanding and the specific requirements of your project.

B. Choosing a Self-Adjusting Data Structure
Hash Table Suitability: Hash tables are efficient for quick lookups, updates, and managing unique identifiers like package IDs. Assess how a hash table can interact with your chosen algorithm.

Data Relationships: Understand how each piece of data is related (e.g., package ID to delivery address) and how this impacts your choice of data structure.

C. Program Overview
Pseudocode: Write pseudocode for your chosen algorithm. This helps in clarifying the logic and steps involved.

Programming Environment: Choose your programming environment (Python IDE, hardware specifications) that supports your development needs.

Space-Time Complexity: Evaluate the Big-O notation for your program. This includes understanding the complexity of your algorithm and data structure separately and in combination.

Scalability Analysis: Assess how your program can adapt to a growing number of packages, different cities, or changing delivery conditions.

Software Design Efficiency: Look into how your software design supports maintenance and efficiency. Modular design, for instance, can be beneficial.

Data Structure Analysis: Discuss the strengths and weaknesses of your chosen data structure, particularly in the context of your application.

Key Choice Justification: Choose a key (e.g., package ID, delivery address) for your hash table that optimizes delivery management, and justify your choice.

D. Documentation and Citation
Properly document your code and decisions.
Acknowledge all sources of information and inspiration, following appropriate academic standards for citation.
E. Professional Communication
Ensure that your documentation and code comments are clear, concise, and professional.
Prepare to present your findings in a manner understandable to both technical and non-technical stakeholders.
Testing and Evaluation
Implement a Prototype: Develop a basic version of your program.
Test Cases: Create test scenarios based on the WGUPS scenario to evaluate each algorithm's performance.
Iterative Testing: Run tests, gather data, and compare against your efficiency criteria.
Adjustments and Optimization: Based on test results, make necessary adjustments to your algorithm or data structure.
Conclusion
Final Selection: Decide on the best-performing algorithm based on empirical evidence from your tests.
Justification and Reporting: Prepare a detailed report justifying your choices and explaining the efficiency of your final solution.
Remember, the goal is not just to find the most efficient algorithm in theory but one that works best under the specific constraints and requirements of your project scenario.


----------------------------------


based on the assumptions of the task. how would the nearest neighbor algorithm work if there are extra requirements for each package like (Can only be on truck 2, Delayed on flight---will not arrive to depot until 9:05 am, Wrong address listed, Must be delivered with 15, 19, etc.)
ChatGPT
The Nearest Neighbor Algorithm is a heuristic that can be used to approach the solution to the traveling salesman problem, which is similar to the challenge of routing delivery trucks efficiently. However, when there are additional constraints attached to each package, such as specific truck assignments, delivery time windows, or grouped delivery requirements, the standard Nearest Neighbor Algorithm needs to be adapted. Here's how you might approach this:

Pre-Processing Phase:

Package Constraints: Before starting the route, analyze all packages for any special notes or constraints (e.g., "Can only be on truck 2", "Delayed on flight", "Wrong address listed", "Must be delivered with 15, 19").
Sorting and Grouping: Organize packages based on their constraints. For instance, group together packages that must be delivered together or sort packages that have a specific start time.
Address Corrections: Implement a system to update addresses at specified times (e.g., for package #9 after 10:20 am).
Route Planning Phase:

Multiple Iterations: Use the Nearest Neighbor Algorithm in multiple iterations for each truck, especially if trucks return to the depot to pick up additional packages.
Constraint Satisfaction: For each iteration, start with packages that have the most constraints (e.g., latest start time, specific truck requirement) and plan their delivery first.
Dynamic Adjustment: As new packages arrive (e.g., delayed on a flight), dynamically adjust the route to include these packages in the nearest neighbor search.
Routing Algorithm:

Step-by-Step Execution:
Start Point: Begin at the hub or the last delivery point.
Find Nearest: Identify the nearest deliverable package that meets the current truck's constraints.
Check Constraints: Ensure the selected package doesn't violate any constraints of the packages already in the truck or yet to be delivered.
Delivery: "Deliver" the package and mark it as such.
Repeat: Continue until all packages for that iteration are delivered or the truck needs to return to the hub.
Constraint Handling:

Specific Truck Only: Reserve space on the designated truck for such packages and plan routes for other packages accordingly.
Delayed Packages: Start the route with packages available at the depot and adjust the route to include the delayed packages once they arrive.
Incorrect Address: If an address is known to be wrong, plan the delivery for after the correction time or use a placeholder address if the correct one can be estimated.
Grouped Deliveries: Treat packages that must be delivered together as a single unit for the purpose of the nearest neighbor search.
Post-Processing Phase:

Verification: After the initial plan is created, verify that all constraints are met.
Optimization: Look for opportunities to optimize the route, such as combining deliveries that are near each other even if they weren't the absolute nearest neighbors.
Real-time Adjustments:

Monitor Progress: As deliveries are made, track the progress of each truck.
Adjust Routes: If an unexpected event occurs (like traffic or a new constraint comes in), be prepared to adjust routes on the fly.
Incorporating these additional steps and considerations into the Nearest Neighbor Algorithm allows it to work within the constraints of the specific scenario provided by the WGUPS Routing Program. However, the Nearest Neighbor Algorithm is not necessarily the most efficient solution for problems with constraints this complex, and other algorithms or even a combination of several may be required to find a more optimal solution.


----------------------------------
NOTES: Priority status can be used to determine which packages are delivered first. Packages with a priority status of "High" should be delivered first, followed by packages with a priority status of "Medium", and finally packages with a priority status of "Low". If two packages have the same priority status, they should be delivered in order of their deadline. For example, if two packages have a priority status of "High", the package with the earliest deadline should be delivered first. If two packages have the same priority status and deadline, they should be delivered in order of their ID number. For example, if two packages have a priority status of "High" and a deadline of 9:00 am, the package with the lower ID number should be delivered first. If two packages have the same priority status, deadline, and ID number, they can be delivered in any order. For example, if two packages have a priority status of "Medium", a deadline of 10:30 am, and an ID number of 13, they can be delivered in any order. If a package has a deadline of EOD, it should be delivered at the end of the day. If a package has a deadline of 10:30 am, it should be delivered by 10:30 am. 

If a package has a short delivery window, for example a package that is arriving late and has to be picked up back at the warehouse, and the deadline is 2 hours later, are considered high priority. As soon as the package is picked up from the warehouse, it should be delivered to the address as soon as possible, only if there are no other near by locations to delivery to first. If there are a few (2 - 3) other locations to deliver to first, then the high priority package can wait a little bit longer to be delivered.
Package #25 from the excel has a high priority becuase it was delayed on flight and won't arrive until 9:05am, but the deadline is 10:30am. So, it should be delivered as soon as possible
Package #26 is low priority, and has to be delivered to the same location or close location as package #25. So, it can be delivered after package #25 is delivered.

There are other cases where the address was listed wrong. 


Main Priority Goal: do not use so much milage on trucks. 
Secondary Priority Goal: deliver packages on time.
Tertiary Priority Goal: if special ocasions arise, like a package is delayed on flight, then the package can be delivered accordingly


Questions:
- which locations should be delivered to first and by which truck if one of the trucks has to go back to the warehouse to pick up a package that was delayed on flight?
- when should the algorithm choose to go back to the warehouse to pick up a package that was delayed on flight?

notes:
- one or both trucks can go back to the warehouse to pick up a package that was delayed on flight
    - if a group of late arrival packages are close together and another group of late arrival packages are also close. then one truck can go to the first group and the other truck can go to the second group.

functions:
- assign packages to trucks, happens before they leave the warehouse
    - when assigning packages to trucks, we want to split the packages into N groups, where N is the number of trucks that will be occupied.
    - make sure there are no more than 16 packages at a time on a truck
        - each group has the smallest total distance to travel
    - keeping in mind the packages that will arrive late at the warehouse, plan ahead so that one or both of the trucks can go back to the warehouse to pick up the late arrival packages. a second truck will not go back to the warehouse if the total distance to travel is less than the distance to the warehouse and back with newly added packages. 
        - out of the late arrival packages, add them to the graph with the other packages and find the shortest path to the late arrival packages. do it for N number of trucks to see which truck will get assigned the return to warehouse task.

Objects:
- Dispatcher: is in charge of assigning packages and a route to each truck at any stopped location (including before the trucks leave the warehouse)
    - assign packages to trucks
    - assign routes to trucks
    - assign a return to warehouse task to a truck
- Truck: is in charge of delivering packages to their destinations
- Driver: is in charge of driving the truck to its destination
- Package: holds the package information, ID number, address, deadline, weight, special notes, etc.
- Location: holds the location information, address, latitude, longitude, etc.
- LocationGraph: holds the location information and the distance between each location so that the shortest path can be found


- Dispatcher
    - order the packages by earliest deadline first
    - 
    - Explore() the graph to find the shortest path to each location (up to 16 packages) for the first truck. the first truck is preferribly the truck that has been explicitly assigned packages, so that the rest of the trucks can be assigned packages that are left over. note the first truck can have an ID of 2, 3, or 4.
    - the next priority is to assign packages to the truck that have to be in groups.
    - remove the routed packages from the first route and assign the remaining packages (or up to 16 packages) to the next available truck(truck with driver) using the same algorithm as before. repeat until all packages have been assigned to a truck.

Self Adjusting Algorithm:
- Genetic Algorithm