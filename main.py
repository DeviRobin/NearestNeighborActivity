# Devika Prasanth
# 010101895
import datetime
from datetime import datetime
from packages import WGUPackage, update_package_9_address
import HashMap
import trucks
import csv
import numpy as np

with open("distanceCSV.csv", "r") as distanceCSV:
    deliveryDistance = csv.reader(distanceCSV)
    deliveryDistance = [
        [float(value) if value else None for value in row] for row in deliveryDistance
    ]
    # #convert to distance matrix
    distanceMatrix = np.array(deliveryDistance, dtype=float)   #dimensions = distanceMatrix.shape
    # fill in top of adjacency matrix
    rows, cols = distanceMatrix.shape
    for i in range(rows):
        for j in range(i + 1, cols):
            if np.isnan(distanceMatrix[i][j]) or distanceMatrix[i][j] == 0.0:
                distanceMatrix[i][j] = distanceMatrix[j][i]
    distanceMatrix = np.nan_to_num(distanceMatrix)
    # print(distanceMatrix)   -test

with open("addressCSV.csv", "r") as addressCSV:
    deliveryAddress = csv.reader(addressCSV)
    deliveryAddress = list(deliveryAddress)
    # print(deliveryAddress) - test

#Building Dictionaries to for address and index look up
def build_address_lookup(address_list):
    address_to_index = {}
    address_to_location = {}
    index_to_address = {}
    for row in address_list:
        index = int(row[0])  #index to integer
        location = row[1]
        address = row[2]

        address_to_index[address] = index
        address_to_location[address] = location
        index_to_address[int(index)] = address
    return address_to_index, address_to_location, index_to_address
address_to_index, address_to_location, index_to_address = build_address_lookup(deliveryAddress)

#Code derived from (Tepe, Getting Greedy, Who Moved My Data, 2020 WGU) educational material
def load_package_data(file_name):
    with open(file_name) as packageCSV_file:
        packageInfo = csv.reader(packageCSV_file)
        next (packageInfo) #skip header
        for package in packageInfo:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZIP = int(package[4])
            pDeadline = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = "HUB"

            #package object
            loadedPackage = WGUPackage(pID, pAddress, pCity, pState, pZIP, pDeadline, pWeight, pNotes, pStatus)
            #print(loadedPackage)

            #insert it into hashtable
            packageHash.insert(pID, loadedPackage)

packageHash = HashMap.ChainingHashTable()
load_package_data('packageCSV.csv')

#Look up package ny ID function
def lookup_package_by_ID(packageID,):
    package = packageHash.search(packageID)
    if package is not None:
        return (f"""
            Package ID: {package.packageID} 
            Delivery Address:{package.address}
            Delivery Deadline: {package.deadline}
            City: {package.city}
            ZIP Code: {package.zip}
            Package Weight: {package.weight}
            Delivery Status: {package.deliveryStatus}
            Delivery Time: {package.deliveryTime}
            """)
    else:
        return {"Error": f"Package ID {packageID} not found"}

# initialize trucks and manually load with packages
truck1 = trucks.DeliveryTrucks(1, 0.0, "Western Governors University",
                               "08:00 AM", [1, 7, 8, 13, 14, 15, 16, 19, 20, 29, 30, 34, 37, 39, 40])
truck2 = trucks.DeliveryTrucks(2, 0.0, "Western Governors University",
                               "09:05 AM", [2, 3, 6, 12, 17, 18, 25, 27, 28, 32, 33, 35, 36, 38])
truck3 = trucks.DeliveryTrucks(3, 0.0, "Western Governors University",
                               "10:11 AM" , [4, 5, 9, 10, 11, 21, 22, 23, 24, 26, 31])

def deliver_packages(truck):
    current_index = 0  # Start at the hub/Western Governors University
    total_distance = 0.0  # Keep track of total distance
    unvisited_packages = truck.tpackages[:]  # Copy of all packages in the truck

    # Assign the truck ID to each package for records
    for pkg_id in unvisited_packages:
        package = packageHash.search(pkg_id)
        package.set_package_deliveryTruck(truck.tID)

    while len(unvisited_packages) > 0:  # Continue until all packages are delivered

        # Find the nearest package with the earliest deadline
        nearest_pkg_id = None
        shortest_distance = float('inf')
        earliest_deadline = datetime.max
        # iterate through packages in the unvisited package list
        for pkg_id in unvisited_packages:
            package = packageHash.search(pkg_id) #search has for id in hash
            destination_index = address_to_index[package.address] # check dict for index by package address
            distance = float(distanceMatrix[current_index][destination_index]) # use adjacency matrix
            # Skip Package 9 if it is before 10:20 AM
            if pkg_id == 9 and truck.tTime < datetime.strptime("10:20 AM", "%I:%M %p"):
                continue
            else:
                update_package_9_address(packageHash, truck.tTime)  # Handle special case for Package 9
            # Determine if this package has the earliest deadline and is closer
            package_deadline = (
                datetime.strptime(package.deadline, "%I:%M %p")
                if package.deadline != "EOD"
                else datetime.max
            )
            if package_deadline < earliest_deadline or (
                    package_deadline == earliest_deadline and distance < shortest_distance
            ):
                nearest_pkg_id = pkg_id
                shortest_distance = distance
                earliest_deadline = package_deadline

        if nearest_pkg_id is None:
            break  # Safeguard against empty lists/run out off packages

        # Deliver the nearest package with the earliest deadline
        package = packageHash.search(nearest_pkg_id)
        truck.travel_time(shortest_distance)
        truck.update_mileage(shortest_distance)
        truck.deliver_package(package)

        # Remove from unvisited packages
        unvisited_packages.remove(nearest_pkg_id)
        current_index = address_to_index[package.address]  # Update current location
        total_distance += shortest_distance

        # Return to the hub and update truck properties
    hub_distance = float(distanceMatrix[current_index][0])
    truck.travel_time(hub_distance)
    truck.update_mileage(hub_distance)
    truck.update_status("Completed Deliveries - At Hub")

    # print(f"""
    #         Truck {truck.tID}
    #         Return to Hub at: {truck.tTime.strftime('%I:%M:%p')}
    #         Mileage: {truck.tmileage:.2f}
    #         Current Status: {truck.tstatus}
    #         """) - for test
    return truck.tmileage, truck.tTime.strftime('%I:%M:%p')

#function to simulate delivery of all packages, ensures truck 3 does not leave until truck 1 is at hub.
def finish_it_up(truck1, truck2, truck3):
    deliver_packages(truck1)
    deliver_packages(truck2)
    if truck1.tstatus == "Completed Deliveries - At Hub":
        deliver_packages(truck3)

AllTrucks = [truck1,truck2,truck3] # a list of all delivery trucks to iterate through

def view_packages_status_by_time(userInput, all_trucks):
    userInputTime = datetime.strptime(userInput, "%I:%M %p")  # Convert input time to datetime object
    print(f"\nPackage Status at {userInputTime.strftime('%I:%M %p')}:\n")
    for truck in all_trucks:
        print(f"Truck {truck.tID} at {userInputTime.strftime('%I:%M %p')}: ")
        print(f"Mileage: {truck.get_mileage():.2f}")
        print(f"  Packages:")
        for pkg_id in truck.tpackages:
            package = packageHash.search(pkg_id)
            if pkg_id == 9: # this will be used for special case as the address is 300 State St before and 410 S after 10:20 AM.
                if userInputTime <= datetime.strptime("10:20 AM",'%I:%M %p'):
                    package_status = f"DELIVERY ADDRESS: 300 State St | DEADLINE: {package.deadline} | STATUS : En route | TruckID : {truck.tID} "
                else:
                    package_status = f"DELIVERY ADDRESS: 410 S State St | DEADLINE: {package.deadline} | STATUS : En route | TruckID : {truck.tID}"
            else:
                if package.deliveryTime is None:  # Not yet delivered
                    if userInputTime < truck.tstartTime:  # Before the truck departs
                        package_status = f"DELIVERY ADDRESS: {package.address} | DEADLINE: {package.deadline} | STATUS : AT HUB | TruckID : To be loaded "
                    else:  # After the truck departs
                        package_status = f"DELIVERY ADDRESS: {package.address} | DEADLINE: {package.deadline} | STATUS : EN ROUTE | TruckID : {truck.tID}"
                else:  # Package has a delivery time
                    delivery_time = datetime.strptime(package.deliveryTime, "%H:%M %p")
                    if userInputTime < truck.tstartTime:  # Before the truck departs
                        package_status = f"DELIVERY ADDRESS: {package.address} | DEADLINE: {package.deadline} | STATUS : AT HUB | TruckID : To be loaded "
                    elif truck.tstartTime <= userInputTime < delivery_time:  # After departure but before delivery
                        package_status = f"DELIVERY ADDRESS: {package.address} | DEADLINE: {package.deadline} | STATUS : EN ROUTE | TruckID : {truck.tID} "
                    else:  # After delivery
                        package_status = f"DELIVERY ADDRESS: {package.address} | DELIVERY TIME: {package.deliveryTime} | DEADLINE: {package.deadline} | STATUS : DELIVERED | TruckID : {truck.tID} "

            # Print the package details
            print(f"    Package {pkg_id}: {package_status}")

        print("-----------------------------------------------------------------------------------------")

#Run Simulation of All Trucks
finish_it_up(truck1,truck2, truck3)

#Calculate total Mileage of All trucks
total_mileage_all_trucks = truck1.get_mileage() + truck2.get_mileage() + truck3.get_mileage()
"""
Part D - Provide an intuitive interface:
This interface  uses exception handling to give user another chance to enter the time correctly if they fail the first time. 
User can see the total milage of all trucks at top of output screen. The user will then be prompted to enter in a time using
a 12hr HH:MM AM/PM format. 
This user input will then be converted into a datetime object so it can be compared the package delivery times. 

"""
#will loop until END is entered into the input
#Will go though prompts to allow user to see package detailes, mileage, and package status by time
ask_again = True
while ask_again:
    startInput = input("1. Get Total Mileage\n2. See status of packages by time\nPlease enter 1 or 2 : ")
    if startInput == "1":
        print(f'\nTotal Mileage of All Trucks: {total_mileage_all_trucks:.2f} \n')
        print(f'Truck 1 : {truck1.get_mileage():.2f} \nTruck 2 : {truck2.get_mileage():.2f} \nTruck 3 : {truck3.get_mileage():.2f}\n')
    elif startInput == "2":
        userInput = input("Please enter a time (HH:MM AM/PM) to see the status of all packages or type END to exit: ")
        try: # error handling to address if wrong format is used in input
            if  userInput == "END":
                print("Bye!")
                ask_again = False
            else:
                view_packages_status_by_time(userInput, AllTrucks)
        except ValueError:
            print("You have either entered an invalid time, or used the wrong format. Enter time in 12hr HH:MM AM/PM format")
    else: print("You have entered an invalid input, please try again")

