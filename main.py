# Devika Prasanth
# 010101895


import datetime
from datetime import datetime
from packages import WGUPackage, update_package_9_address
import HashMap
import trucks
import csv
import numpy as np
from trucks import DeliveryTrucks

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

#Building Dictionaries
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

def get_index_by_address(address, address_to_index):
    return address_to_index.get(address,None) #will get index of when address is entered

def get_location_by_address(address, address_to_location):
    return address_to_location.get(address,None)

def get_address_by_index(index, index_to_address):
    return index_to_address.get(int(index),None)

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
# Test Package Hash Table
# for i in range (len(packageHash.table)+1):
#    print("Key: {} and Package Info {}".format(i+1, packageHash.search(i+1))) #1 to 40 is sent to packageHash.search()



# initialize trucks and manually load with packages
truck1 = trucks.DeliveryTrucks(1, 0.0, "Western Governors University", "08:00 AM", [1, 7, 8, 13, 14, 15, 16, 19, 20, 29, 30, 34, 37, 39, 40])
truck2 = trucks.DeliveryTrucks(2, 0.0, "Western Governors University", "09:05 AM", [2, 3, 6, 12, 17, 18, 25, 27, 28, 32, 33, 35, 36, 38])
truck3 = trucks.DeliveryTrucks(3, 0.0, "Western Governors University", "10:00 AM" , [4, 5, 9, 10, 11, 21, 22, 23, 24, 26, 31]) #datetime.datetime.strptime(truck1.get_truck_time(),'%I:%M %p')


def optimize_via_clustering(truck_packages):
    clusters = [] # list to store clusters of packages
    clustered_addresses = set() #set to keep track of addresses already clustered

    #Iterate through all packages on the truck
    for pkg_id in truck_packages:
        package = packageHash.search(pkg_id) #get package details from hash
        current_address = package.address # set the current address as package address

        #this ensures that addresses that are already clustered will be skipped
        if current_address in clustered_addresses:
            continue

        # Create a new cluster for this address
        cluster = [pkg_id]
        clustered_addresses.add(current_address) #adds current address to list of already clustered
        # get index of current address using the adjacency matrix
        current_index = address_to_index[current_address]
        # find other packages close to this package
        for other_pkg_id in truck_packages: #iterate through the other packages on truck
            if other_pkg_id == pkg_id:# makes sure we are looking at other packages and not current one
                continue
            other_package = packageHash.search(other_pkg_id) # get the other packages details
            other_index = address_to_index[other_package.address]
            distance = float(distanceMatrix[current_index][other_index]) # get the distance between the current package index and the other package
            # Include packages within a threshold distance
            if distance <= 2.0: # sets threshold distance ( in this case 2 miles)
                cluster.append(other_pkg_id) # adds the close package to the id cluster
                clustered_addresses.add(other_package.address) # makes sure the address is added to already clustered addresses

        clusters.append(cluster) # add the newly formed cluster to the list of clusters

    return clusters


def deliver_packages(truck):
    current_index = 0  # Start at the hub/Western Governors University
    total_distance = 0.0  # Keep track of total distance
    unvisited_packages = truck.tpackages[:]  # Copy of all packages in the truck

    # Assign the truck ID to each package for records
    for pkg_id in unvisited_packages:
        package = packageHash.search(pkg_id)
        package.set_package_deliveryTruck(truck.tID)

    while len(unvisited_packages)>0: # will continue until there are no unvisited packages
        # Update package 9's address if it is past 10:30 AM
        update_package_9_address(packageHash, truck.tTime)

        # call the clustering function to create a list of clusters
        clusters = optimize_via_clustering(unvisited_packages)

        for cluster in clusters:
            # Sort the packages in each cluster by their delivery deadline
            #using a lambda function as key for sort to avoid new fucntion, and for clarity
            cluster.sort(key=lambda pkg_id: (
                datetime.strptime(packageHash.search(pkg_id).deadline, "%I:%M %p") # will get deadline
                if packageHash.search(pkg_id).deadline != "EOD" # if deadline is not EOD it will be prioritized
                else datetime.max # if the deadline is EOD then it the deadline will be declared the maximum time available/ the lowest priority
            ))
            #While clusters remain on the list
            while len(clusters)>0:
                # Find the nearest package within the cluster
                nearest_pkg_id = None       # initializing variables
                shortest_distance = float('inf')  # sets the shortest distance to the largest number

                for pkg_id in cluster: #for each package
                    package = packageHash.search(pkg_id) # a look-up package details in hash
                    destination_index = address_to_index[package.address] # destination index will be found from dict
                    distance = float(distanceMatrix[current_index][destination_index]) #fdistance will be looked up on adjacency matrix via index
                    #Identify the package with the shortest distance to current package
                    #SPECIAL Case for package 9 so it isn't delivered before it is updated.
                    if pkg_id == 9 and truck.tTime < datetime.strptime("10:20 AM", "%I:%M %p"):
                        continue

                    if distance < shortest_distance:
                        nearest_pkg_id = pkg_id
                        shortest_distance = distance

                if nearest_pkg_id is None:
                    break  # Safeguard against empty clusters

                # Deliver the nearest package
                package = packageHash.search(nearest_pkg_id)
                truck.travel_time(shortest_distance)
                truck.update_mileage(shortest_distance) # update truck
                truck.deliver_package(package) #update package status and time of delivery

                # Remove from cluster and unvisited_packages if present
                cluster.remove(nearest_pkg_id) # remove from cluster
                if nearest_pkg_id in unvisited_packages: # if in unvisited package list - remove
                    unvisited_packages.remove(nearest_pkg_id)
                current_index = address_to_index[package.address] # update current location
                total_distance += shortest_distance # update total distance

    # Return to the hub
    hub_distance = float(distanceMatrix[current_index][0]) # calculates distance to hub
    truck.travel_time(hub_distance) # update truck time when it reaches hub
    truck.update_mileage(hub_distance) #update truck mileage
    truck.update_status("Completed Deliveries - At Hub") # will update status of truck

    print(f"""
            Truck {truck.tID} 
            Return to Hub at: {truck.tTime.strftime('%I:%M:%p')} 
            Mileage: {truck.tmileage:.2f}
            Current Status: {truck.tstatus}
            """)
    return truck.tmileage, truck.tTime.strftime('%I:%M:%p')

#function to simulate delivery of all packages, ensures truck 3 does not leave until truck 1 is at hub.
def finish_it_up(truck1, truck2, truck3):
    deliver_packages(truck1)
    deliver_packages(truck2)
    if (truck1.tstatus == "Completed Deliveries - At Hub") :
        deliver_packages(truck3)

AllTrucks = [truck1,truck2,truck3] # a list of all delivery trucks to iterate through
def view_packages_status_by_time(userInput, all_trucks):

    userInputTime = datetime.strptime(userInput, "%I:%M %p")  # Convert input time to datetime object

    print(f"\nPackage Status at {userInputTime.strftime('%I:%M %p')}:\n")
    for truck in all_trucks:
        print(f"Truck {truck.tID} at {userInputTime.strftime('%I:%M %p')}: ")
        print(f"Mileage: {truck.get_mileage()}")
        print(f"  Packages:")

        for pkg_id in truck.tpackages:
            package = packageHash.search(pkg_id)
            if package.deliveryTime is None:  # Not yet delivered
                if userInputTime < truck.tstartTime:  # Before the truck departs
                    package_status = "At the Hub"
                else:  # After the truck departs
                    package_status = f"En route on Truck {truck.tID}"
            else:  # Package has a delivery time
                delivery_time = datetime.strptime(package.deliveryTime, "%H:%M %p")
                if userInputTime < truck.tstartTime:  # Before the truck departs
                    package_status = "At the Hub"
                elif truck.tstartTime <= userInputTime < delivery_time:  # After departure but before delivery
                    package_status = f"En route on Truck {truck.tID}"
                else:  # After delivery
                    package_status = f"Delivered to {package.address} at {package.deliveryTime}"

            # Print the package details
            print(f"    Package {pkg_id}: {package_status}")

        print("-----------------------------------------------------------------------------------------")

#Run Simulation of All Trucks
finish_it_up(truck1,truck2, truck3)

#Calculate total Mileage of All trucks
total_mileage_all_trucks = truck1.get_mileage() + truck2.get_mileage() + truck3.get_mileage()

"""
Part D - Provide an intuitive interface for the user to view the delivery status (including the delivery time) of any 
package at any time and the total mileage traveled by all trucks. (The delivery status should report the package as at 
the hub, en route, or delivered. Delivery status must include the time.)
    
This interface  uses exception handling to give user another chance to enter the time correctly if they fail the first time. 
User can see the total milage of all trucks at top of output screen. The user will then be prompted to enter in a time using
a 12hr HH:MM AM/PM format. 
This user input will then be converted into a datetime object so it can be compared the package delivery times. 

"""
# Prints TOTAL Mileage of All Trucks
print(f'Total Mileage of All Trucks: {total_mileage_all_trucks:.2f} \n')  # 122.70 total Mileage of all Trucks

#will loop until END is entered into the input
ask_again = True
while ask_again:
    userInput = input("Please enter a time (HH:MM AM/PM) to see the status of all packages or type END to exit: ")
    try: # error handling to address if wrong format is used in input
        if  userInput == "END":
            print("Bye!")
            ask_again = False
        else:
            view_packages_status_by_time(userInput, AllTrucks)
    except ValueError:
        print("You have either entered an invalid time, or used the wrong format. Enter time in 12hr HH:MM AM/PM format")


