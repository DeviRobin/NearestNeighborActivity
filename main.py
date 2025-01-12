
from datetime import timedelta
import datetime
from packages import WGUPackage
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
truck1 = trucks.DeliveryTrucks(1, 0.0, "Western Governors University", ("08:00 AM"), [15, 16, 19, 20, 29, 30, 34, 37, 39, 40, 1, 7, 8, 13, 14])
truck2 = trucks.DeliveryTrucks(2, 0.0, "Western Governors University", ("09:05 AM"), [6,25,2,3,12,17,18,27,28,32,33,35,36,38])
truck3 = trucks.DeliveryTrucks(3, 0.0, "Western Governors University",("10:30 AM"), [9,4,5,10,11,21,22,23,24,26,31])


def find_nearest_neighbor(current_index, unvisited_indices, distanceMatrix):
    nearest_index = None
    shortest_distance = float('inf')

    for index in unvisited_indices:
        distance = float(distanceMatrix[current_index][index])
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_index = index
    return nearest_index, shortest_distance


def deliver_packages(truck):

    current_index = 0  # Start at the hub
    unvisited_packages = {pkg_id for pkg_id in truck.tpackages} # creates  a set of
    unvisited_indices = {address_to_index[packageHash.search(pkg_id).address] for pkg_id in unvisited_packages}

    for pkg_id in list(unvisited_packages):
        package = packageHash.search(pkg_id)
        package.set_package_deliveryTruck(truck.tID)

    while len(unvisited_packages) > 0:
        # Find the nearest neighbor
        nearest_index, distance = find_nearest_neighbor(current_index, unvisited_indices, distanceMatrix)
        # Update truck's total distance and time
        #total_distance += distance
        truck.travel_time(distance)
        truck.update_mileage(distance)
        # current_time += travel_time
        # Deliver all packages at the current location
        for pkg_id in list(unvisited_packages):
            package = packageHash.search(pkg_id)
            if address_to_index[package.address] == nearest_index:
                truck.deliver_package(package)
                unvisited_packages.remove(pkg_id)
               # return print(package, truck.tlocation, truck.tTime)

        # Update current location and remove from unvisited indices
        current_index = nearest_index
        unvisited_indices.remove(nearest_index)

    # Return to the hub
    hub_distance = float(distanceMatrix[current_index][0])
    truck.travel_time(hub_distance)
    truck.update_mileage(hub_distance)
    return truck.tmileage, truck.tTime.strftime('%H:%M:%S')


mileage, end_time = deliver_packages(truck1)
print(f"Truck 1 completed deliveries with total mileage: {mileage:.2f} and end time: {end_time}")

