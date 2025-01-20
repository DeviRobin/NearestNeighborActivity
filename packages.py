# Devika Prasanth
# 010101895
import datetime
from datetime import datetime
"""
Initializes WGUPackage class
Function: 
    lookup_package_by_ID: Part B - look-up function that takes the package ID as input and returns package details
    update_package_9_address: function to update package 9 at 10:20 AM when WGUPS gets correct address
"""
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
        self.deliveryStatus = "Hub"
        self.deliveryTime = None
        self.deliveryTruck = None

    def __str__(self):
        return (f" Package: {self.packageID} Address: {self.address} City: {self.city} State:{self.state} "
                f"ZIP:{self.zip} Deadline:{self.deadline} Weight:{self.weight} Notes:{self.notes} "
                f"Status:{self.deliveryStatus} Delivery:{self.deliveryTime} Truck:{self.deliveryTruck}")

    def set_package_status(self,nstatus):
        self.deliveryStatus = nstatus

    def set_package_deliveryTime(self, ndeliveryTime):
        self.deliveryTime = ndeliveryTime

    def set_package_deliveryTruck(self, truckID):
        self.deliveryTruck = truckID

# This is a function to update package 9 at 10:20 am when WGUPS is made aware of the correct address
def update_package_9_address(packageHash, truck_time):
    update_time = datetime.strptime("10:20 AM", "%I:%M %p")
    package_9 = packageHash.search(9)

    if truck_time >= update_time:
        if package_9:
            package_9.address ="410 S State St"
            package_9.city = "Salt Lake City"
            package_9.zip = 84111
            print("Package #9 address updated to 410 S. State St., Salt Lake City, UT 84111")
