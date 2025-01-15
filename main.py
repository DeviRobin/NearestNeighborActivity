# Devika Prasanth
# 010101895

from datetime import timedelta
import datetime

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
    print(distanceMatrix)

with open("addressCSV.csv", "r") as addressCSV:
    deliveryAddress = csv.reader(addressCSV)
    deliveryAddress = list(deliveryAddress)
    print(deliveryAddress)

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
truck1 = trucks.DeliveryTrucks(1, 0.0, "Western Governors University", ("08:00 AM"), [1, 7, 8, 13, 14, 15, 16, 19, 20, 29, 30, 34, 37, 39, 40])
truck2 = trucks.DeliveryTrucks(2, 0.0, "Western Governors University", ("09:05 AM"), [2, 3, 6, 12, 17, 18, 25, 27, 28, 32, 33, 35, 36, 38])
truck3 = trucks.DeliveryTrucks(3, 0.0, "Western Governors University",("10:00 AM") , [4, 5, 9, 10, 11, 21, 22, 23, 24, 26, 31])
#NOTE!: MAKE SURE TO MAKE AN EXECTE FCT TO MAKE SURE TRUCK THREE ONLY STARTS WHen truck 1 IS BACK!!!

# def find_nearest_neighbor(current_index, unvisited_indices, distanceMatrix):
#     nearest_index = None
#     shortest_distance = float('inf')
#
#     for index in unvisited_indices:
#         distance = float(distanceMatrix[current_index][index])
#         if distance < shortest_distance:
#             shortest_distance = distance
#             nearest_index = index
#     return nearest_index, shortest_distance

#Prioritize packages in the truck package list based on deadlines
#using nested function for clarity
def prioritize_packages(truck_packages, packageHash):
    def deadline_sort_key(package_id):
        package = packageHash.search(package_id)
        if package.deadline == "EOD":
            return datetime.datetime.max  # Sets the string "EOD" as the latest possible deadline
        else:
            return datetime.datetime.strptime(package.deadline, "%I:%M %p")
    return sorted(truck_packages, key=deadline_sort_key)

def find_nearest_package(current_index, unvisisted_packages, truck, distanceMatrix, packageHash):
    nearest_package = None
    nearest_index = None
    shortest_distance = float('inf')
    highest_priority = float('inf') # In this case a smaller value will = higher priority. so infinity is the lowest priority

    for pkg_id in unvisisted_packages:
        package = packageHash.search(pkg_id)
        destination_index = address_to_index[package.address]
        distance = float(distanceMatrix[current_index][destination_index])

        #calculating time to reach a destination
        travel_time = timedelta(hours=distance / truck.tspeed)
        expected_delivery_time = truck.tTime + travel_time

        #Check to see if package is EOD or has deadline, prioritizes deadline packages
        if package.deadline != "EOD":
            deadline = datetime.datetime.strptime(package.deadline, "%I:%M %p")
            priority = (deadline - expected_delivery_time).total_seconds()
        else:
            priority = float('inf') # sets EOD packages with lower priority

        # sets nearest package taking into account priority first, and then distance.
        # if two packages have the same priority the closest will be selected
        if priority < highest_priority or (priority == highest_priority and distance < shortest_distance):
            nearest_package = pkg_id
            nearest_index = destination_index
            shortest_distance = distance
            highest_priority = priority
    return nearest_package, nearest_index, shortest_distance



def deliver_packages(truck):
    current_index = 0  # Start at the hub/Western gov
    unvisited_packages = prioritize_packages(truck.tpackages,packageHash)
    #{pkg_id for pkg_id in truck.tpackages} # creates  a set of
    #unvisited_indices = {address_to_index[packageHash.search(pkg_id).address] for pkg_id in unvisited_packages}

    for pkg_id in list(unvisited_packages):
        package = packageHash.search(pkg_id)
        package.set_package_deliveryTruck(truck.tID)

    while len(unvisited_packages) > 0:
        #update package 9 at 10:30 am
        update_package_9_address(packageHash,truck.tTime)

        #find nearest package ID from list of unvisited packages while considering deadlines
        nearest_package, nearest_index, distance = find_nearest_package( current_index, unvisited_packages, truck, distanceMatrix, packageHash)

        if nearest_package is None: #when we are all out of packages
            break

        # Travel to the nearest location and update truck time
        truck.travel_time(distance)
        truck.update_mileage(distance)

        # Deliver the package
        package = packageHash.search(nearest_package)
        truck.deliver_package(package)
        unvisited_packages.remove(nearest_package)

        # Update the current location
        current_index = nearest_index

        # Return to the hub
    hub_distance = float(distanceMatrix[current_index][0])
    truck.travel_time(hub_distance)
    truck.update_mileage(hub_distance)

    print(
        f"""
        Truck: {truck.tID} 
        Returned to Hub at: {truck.tTime.strftime('%H:%M:%S')} 
        Mileage: {truck.tmileage:.2f}""")
    return truck.tmileage, truck.tTime.strftime('%H:%M:%S')




    #     # Find the nearest neighbor
    #     nearest_index, distance = find_nearest_neighbor(current_index, unvisited_indices, distanceMatrix)
    #     # Update truck's total distance and time
    #     #total_distance += distance
    #     truck.travel_time(distance)
    #     truck.update_mileage(distance)
    #     # current_time += travel_time
    #     # Deliver all packages at the current location
    #     for pkg_id in list(unvisited_packages):
    #         package = packageHash.search(pkg_id)
    #         if address_to_index[package.address] == nearest_index:
    #             truck.deliver_package(package)
    #             unvisited_packages.remove(pkg_id)
    #            # return print(package, truck.tlocation, truck.tTime)
    #
    #     # Update current location and remove from unvisited indices
    #     current_index = nearest_index
    #     unvisited_indices.remove(nearest_index)
    #
    # # Return to the hub
    # hub_distance = float(distanceMatrix[current_index][0])
    # truck.travel_time(hub_distance)
    # truck.update_mileage(hub_distance)
    # return truck.tmileage, truck.tTime.strftime('%H:%M:%S')


mileage, end_time = deliver_packages(truck1)
print(f"Truck 1 completed deliveries with total mileage: {mileage:.2f} and end time: {end_time}")

mileage, end_time = deliver_packages(truck2)
print(f"Truck 2 completed deliveries with total mileage: {mileage:.2f} and end time: {end_time}")

mileage, end_time = deliver_packages(truck3)
print(f"Truck 3 completed deliveries with total mileage: {mileage:.2f} and end time: {end_time}")
# Test Part B look up package function
#print(packages.lookup_package_by_ID(17,packageHash))