from datetime import datetime, timedelta, time
import packages


# def extract_time(dateandtime): #weird little function to get time into good format as days are not simulated in this exercise
#     datetime_object = dateandtime
#     onlytime = datetime_object.time()
#     return onlytime


class DeliveryTrucks:
    def __init__(self, truckID,mileage,current_location,start_time,packages):
        self.tID = truckID
        self.tpackages = packages #list for package IDs
        self.tnumpackages = len(packages)
        self.tcapacity = 16
        self.tlocation = current_location
        self.tspeed = 18
        self.tmileage = mileage #total miles traveled
        self.tTime = datetime.strptime(start_time,"%I:%M %p" ) #time in min using 12 hour clock HH:mm AM/PM following time format used in instructions


    def __str__(self):
        return f"Truck ID: {self.tID} | Capacity: {self.tcapacity} | Packages: {self.tpackages} | NumPackages: {self.tnumpackages} | Current Location: {self.tlocation} | Speed: {self.tspeed} | Milage: {self.tmileage} | Time: {extract_time(self.tTime)} "

    def deliver_package(self,package):
        package.set_package_status("Delivered")
        package.set_package_deliveryTime(self.tTime)
        package.set_package_deliveryTruck(self.tID)
        print(f"Package {package.packageID} delivered at {self.tTime.strftime('%H:%M:%S')}")

    def travel_time(self, distance): #to travel time
        travel_time = timedelta(hours = distance/self.tspeed) #calculate travel time in minutes.
        self.tTime += travel_time #update truck time

    def update_mileage(self, distance):
        self.tmileage += distance  # update mileage
