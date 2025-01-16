from datetime import datetime, timedelta, time
from time import strftime

import packages

"""
Initializes DevliveryTrucks class

Functions: 
    deliver_package: set package status to Delivered and updates delivery time for each package. Prints alerts as each package is delivered
    travel_time: calculates travel time by dividing distance by mph/hr to get hours traveled. Adds travel time to truck time
"""

class DeliveryTrucks:
    def __init__(self, truckID,mileage,current_location,start_time,packages):
        self.tID = truckID
        self.tpackages = packages #list for package IDs
        self.tnumpackages = len(packages)
        self.tcapacity = 16
        self.tlocation = current_location
        self.tspeed = 18
        self.tmileage = mileage #total miles traveled
        self.tstartTime = datetime.strptime(start_time,'%I:%M %p' ) #time in min using 12 hour clock HH:mm AM/PM following time format used in instructions
        self.tTime = datetime.strptime(start_time,'%I:%M %p' ) # will be updated as truck travels
        self.tstatus = "Activated"

    def get_truck_ID(self):
        return self.tID
    def get_truck_time(self):
        return self.tTime
    def get_mileage(self):
        return self.tmileage


    def __str__(self):
        return f"Truck ID: {self.tID} | Capacity: {self.tcapacity} | Packages: {self.tpackages} | NumPackages: {self.tnumpackages} | Current Location: {self.tlocation} | Speed: {self.tspeed} | Milage: {self.tmileage} | Time: {extract_time(self.tTime)} | Status: {self.tstatus} "

    # set package status to Delivered and updates delivery time for each package. Prints alerts as each package is delivered
    def deliver_package(self,package):
        package.set_package_status("Delivered")
        package.set_package_deliveryTime(datetime.strftime(self.tTime,'%I:%M %p'))
        print(f"Package {package.packageID} delivered at {self.tTime.strftime('%I:%M %p')}")

    # calculates travel time by dividing distance by mph/hr to get hours traveled. Adds travel time to truck time
    def travel_time(self, distance): #to travel time
        travel_time = timedelta(hours = distance/self.tspeed) #calculate travel time in minutes.
        self.tTime += travel_time #update truck time

    def update_mileage(self, distance):
        self.tmileage += distance  # update mileage

    def update_status(self, status):
        self.tstatus = status #update status


