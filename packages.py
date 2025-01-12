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
        self.deliveryTime = None
        self.deliveryTruck = None

    def __str__(self):
        return f" Package: {self.packageID} Address: {self.address} City: {self.city} State:{self.state} ZIP:{self.zip} Deadline:{self.deadline} Weight:{self.weight} Notes:{self.notes} Status:{self.deliveryStatus}  Delivery:{self.deliveryTime} Truck:{self.deliveryTruck}"


    def get_packageID(self):
        return self.packageID

    def package_update(self, npackageID, naddress, ncity, nstate, nzip, ndeadline, nweight, nnotes):
        self.packageID = npackageID
        self.address = naddress
        self.city = ncity
        self.state = nstate
        self.zip = nzip
        self.deadline = ndeadline
        self.weight = nweight
        self.notes = nnotes


    def set_package_status(self,nstatus):
        self.deliveryStatus = nstatus

    def get_package_status(self):
        return self.deliveryStatus

    def set_package_deliveryTime(self, ndeliveryTime):
        self.deliveryTime = ndeliveryTime

    def get_package_deliveryTime(self):
        return self.deliveryTime

    def set_package_deliveryTruck(self, truckID):
        self.deliveryTruck = truckID

    def get_package_deliveryTruck(self):
        return self.deliveryTruck