# Student ID: 008884283
# Student: Sean McKnelly
from Truck import Truck
from AllPackagesArray import AllPackagesArray
from HubMatrix import HubMatrix
from Trucks import Trucks
from hashTable import AllPackagesHashTable

# Load the packages array, hash table, matrix of hubs
myArr = AllPackagesArray()
hashTable = AllPackagesHashTable()
hubMatrix = HubMatrix()
hubMatrix.loadHubs()

# Load the trucks
trucks = Trucks(Truck(1), Truck(2), Truck(3))
trucks.truck2.LoadMandatoryPackages(myArr)
trucks.truck1.LoadGroupedPackages(myArr)
trucks.truck3.LoadFuturePackages(myArr)
trucks.truck1.LoadImaginaryPackage()
trucks.LoadPackagesWithSameAddress(myArr)
trucks.LoadEarlyPackages(myArr, hubMatrix)
trucks.LoadRemainingPackages(myArr, hubMatrix)

# Populate the hash table
trucks.QueueHashTable(hashTable)

# Organize the deliveries
trucks.truck1.OrganizePackagesByRoute(hubMatrix)
trucks.truck2.OrganizePackagesByRoute(hubMatrix)
trucks.truck3.OrganizePackagesByRoute(hubMatrix)

# Deliver the packages
trucks.DeliverPackages(hubMatrix, 8, hashTable)

myBool = True
while(myBool):
    myBool = hashTable.OutputPackages(trucks)

