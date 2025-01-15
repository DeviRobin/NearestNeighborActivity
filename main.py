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

def optimize_via_clustering(truck_packages, packageHash, address_to_index, distanceMatrix):
    clusters = [] # list of clustered packages
    visited_addresses = set() #set to keep track of visited addresses

    for pkg_id in truck_packages:
        package = packageHash.search(pkg_id)
        current_address = package.address
        if current_address in visited_addresses:
            continue

        # Create a new cluster for this address
        cluster = [pkg_id]
        visited_addresses.add(current_address)

        # Find other packages close to this address
        current_index = address_to_index[current_address]
        for other_pkg_id in truck_packages:
            if other_pkg_id == pkg_id:
                continue

            other_package = packageHash.search(other_pkg_id)
            other_index = address_to_index[other_package.address]
            distance = float(distanceMatrix[current_index][other_index])

            # Include packages within a threshold distance (e.g., 5 miles)
            if distance <= 2.0:
                cluster.append(other_pkg_id)
                visited_addresses.add(other_package.address)

        clusters.append(cluster)

    return clusters


def deliver_packages(truck):
    current_index = 0  # Start at the hub/Western Governors University
    total_distance = 0.0  # Keep track of total distance
    unvisited_packages = truck.tpackages[:]  # Copy of all packages in the truck

    # Assign the truck ID to each package
    for pkg_id in unvisited_packages:
        package = packageHash.search(pkg_id)
        package.set_package_deliveryTruck(truck.tID)

    while unvisited_packages:
        # Update package 9's address if it is past 10:30 AM
        update_package_9_address(packageHash, truck.tTime)

        # Cluster unvisited packages dynamically
        clusters = optimize_via_clustering(unvisited_packages, packageHash, address_to_index, distanceMatrix)

        for cluster in clusters:
            # Sort the cluster by deadline
            cluster.sort(key=lambda pkg_id: (
                datetime.datetime.strptime(packageHash.search(pkg_id).deadline, "%I:%M %p")
                if packageHash.search(pkg_id).deadline != "EOD"
                else datetime.datetime.max
            ))

            while cluster:
                # Find the nearest package within the cluster
                nearest_pkg_id = None
                shortest_distance = float('inf')

                for pkg_id in cluster:
                    package = packageHash.search(pkg_id)
                    destination_index = address_to_index[package.address]
                    distance = float(distanceMatrix[current_index][destination_index])

                    if distance < shortest_distance:
                        nearest_pkg_id = pkg_id
                        shortest_distance = distance

                if nearest_pkg_id is None:
                    break  # Safeguard against empty clusters

                # Deliver the nearest package
                package = packageHash.search(nearest_pkg_id)
                travel_time = timedelta(hours=shortest_distance / truck.tspeed)
                truck.tTime += travel_time
                truck.update_mileage(shortest_distance)
                truck.deliver_package(package)

                # Remove from cluster and unvisited_packages if present
                cluster.remove(nearest_pkg_id)
                if nearest_pkg_id in unvisited_packages:
                    unvisited_packages.remove(nearest_pkg_id)

                current_index = address_to_index[package.address]
                total_distance += shortest_distance

    # Return to the hub
    hub_distance = float(distanceMatrix[current_index][0])
    truck.travel_time(hub_distance)
    truck.update_mileage(hub_distance)

    print(f"Truck {truck.tID} returned to hub at {truck.tTime.strftime('%H:%M:%S')} with mileage: {truck.tmileage:.2f}")
    return truck.tmileage, truck.tTime.strftime('%H:%M:%S')

mileage, end_time = deliver_packages(truck1)
print(f"Truck 1 completed deliveries with total mileage: {mileage:.2f} and end time: {end_time}")

mileage, end_time = deliver_packages(truck2)
print(f"Truck 2 completed deliveries with total mileage: {mileage:.2f} and end time: {end_time}")

mileage, end_time = deliver_packages(truck3)
print(f"Truck 3 completed deliveries with total mileage: {mileage:.2f} and end time: {end_time}")

