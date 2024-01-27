

from Model.Dispatcher import Dispatcher
from Model.Utils import load_distance_matrix, load_package_data

        

print("Starting Script...");

#create dispatcher object
dispatcher = Dispatcher()

#load distance matrix and package data
load_distance_matrix(dispatcher);
load_package_data(dispatcher);

index = 0;

print("Starting Dispatch ---------------------------------------- \n\n\n");
dispatcher.print_all_truck_status();
dispatcher.print_num_delivered_packages();

#while dispatch is not complete, dispatch a step
while(dispatcher.is_dispatch_complete() == False):

    print("\n\n\nStep ", dispatcher.live_time, "----------------------------------------\n");
    
    dispatcher.dispatchStep();
    dispatcher.print_all_truck_status();
    dispatcher.print_num_delivered_packages();
    index += 1;

if(dispatcher.is_dispatch_complete() == True):
    print("\nDispatch Complete!")




