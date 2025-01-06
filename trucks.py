import datetime

class Trucks:
    def __init__(self, truckID, location, time, speed, mileage, departureTime, packages):
        self.tID = truckID
        self.tlocation = location
        self.ttime = time
        self.tspeed = speed
        self.tmileage = mileage
        self.tdepartureTime = departureTime
        self.tpackages = packages

    def __str__(self):
        return f"Truck ID: {self.tID}  Current Location: {self.tlocation}  Time: {self.ttime}   Speed: {self.tspeed}  Milage: {self.tmileage}  Departure Time: {self.tdepartureTime}  Packages: {self.tpackages}"




