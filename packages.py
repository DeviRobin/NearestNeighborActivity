import csv
import datetime
from datetime import datetime
import trucks

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

"""
Part B -Develop a look-up function that takes the package ID as input and returns each of the following 
corresponding data components:
    •   delivery address
    •   delivery deadline
    •   delivery city
    •   delivery zip code
    •   package weight
    •   delivery status (i.e., at the hub, en route, or delivered), including the delivery time
"""
def lookup_package_by_ID (packageID, packageHash):
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
                Delivery Time: {package.deliveryTime.strftime('%H:%M:%S') if package.deliveryTime else "Not Delivered Yet" }""")
        else:
            return {"Error": f"Package ID {packageID} not found"}
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







