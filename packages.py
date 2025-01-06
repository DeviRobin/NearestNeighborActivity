import csv
import datetime

from HashMap import ChainingHashTable

class WGUPackage:
    def __init__(self,packageID, address, city, state, zip, deadline, weight, notes, delivery_status ):
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.deliveryStatus = delivery_status
        self.departureTime = None
        self.deliveryTime = None
        self.deliveryTruck = None

    def __str__(self):
        return f" Package: {self.packageID} Address: {self.address} City: {self.city} State:{self.state} ZIP:{self.zip} Deadline:{self.deadline} Weight:{self.weight} Notes:{self.notes} Status:{self.deliveryStatus} Departure:{self.departureTime} Delivery:{self.deliveryTime} Truck:{self.deliveryTruck}"

print(WGUPackage)