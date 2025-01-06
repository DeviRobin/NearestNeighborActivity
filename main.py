import csv
from packages import WGUPackage
import HashMap

with open("distanceCSV.csv", "r") as distanceCSV:
    deliveryDistance = csv.reader(distanceCSV)
    deliveryDistance = list(deliveryDistance)

with open("addressCSV.csv", "r") as addressCSV:
    deliveryAddress = csv.reader(addressCSV)
    deliveryAddress = list(deliveryAddress)

# #Code derived from (Tepe, Getting Greedy, Who Moved My Data, 2020 WGU) educational material
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

for i in range (len(packageHash.table)+1):
    print("Key: {} and Movie {}".format(i+1, packageHash.search(i+1))) #1 to 40 is sent to packageHash.search()
