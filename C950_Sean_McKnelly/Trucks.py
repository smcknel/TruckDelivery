from Truck import Truck
from AllPackagesArray import AllPackagesArray
from Package import Package
from HubMatrix import HubMatrix
from hashTable import AllPackagesHashTable

class Trucks:
    # Initializes the 3 trucks
    def __init__(self, truck1, truck2, truck3):
        self.truck1 = truck1
        self.truck2 = truck2
        self.truck3 = truck3

    # Inserts packages into the hash table
    def QueueHashTable(self, hashTable):
        for package in self.truck1.packageArray:
            hashTable.InsertPackage(package.ID)
        for package in self.truck2.packageArray:
            hashTable.InsertPackage(package.ID)
        for package in self.truck3.packageArray:
            hashTable.InsertPackage(package.ID)
        for package in self.truck3.wrongAddressPackages:
            hashTable.InsertPackage(package.ID)
            

    def LoadPackagesWithSameAddress(self, allPackageArray):
        ## Load packages with same address
        self.truck1.LoadPackagesWithSameAddress(allPackageArray)
        self.truck2.LoadPackagesWithSameAddress(allPackageArray)
        self.truck3.LoadPackagesWithSameAddress(allPackageArray)

    # Loads packages with a delivery time of 9 am or 10:30 am from allPackageArray    
    def LoadEarlyPackages(self, allPackageArray, hubMatrix):
        index = 0
        while index < len(allPackageArray.packageArray):
            if "10:30" in allPackageArray.packageArray[index].deliveryTime or "9:00" in allPackageArray.packageArray[index].deliveryTime:
                self.truck2.LoadPackage(allPackageArray.packageArray[index])
                allPackageArray.packageArray.remove(allPackageArray.packageArray[index])
                index -= 1
            index += 1

    # Used after mandatory packages and grouped packages are loaded, and after late delivery packages are "loaded"
    # Also used after 10:30 and 9 AM packages are loaded.

    # Similar to method above, finds truck with nearest hub and less than 17 packages loaded, then loads the package
    # To that truck
    def LoadRemainingPackages(self, allPackageArray, hubMatrix):
        while allPackageArray.packageArray:
            truckNumber = self.FindTruckWithNearestHub(hubMatrix, allPackageArray.packageArray[0])
            if truckNumber == 1:
                self.truck1.LoadPackage(allPackageArray.packageArray[0])
                allPackageArray.packageArray.remove(allPackageArray.packageArray[0])
            elif truckNumber == 2:
                self.truck2.LoadPackage(allPackageArray.packageArray[0])
                allPackageArray.packageArray.remove(allPackageArray.packageArray[0])
            elif truckNumber == 3:
                self.truck3.LoadPackage(allPackageArray.packageArray[0])
                allPackageArray.packageArray.remove(allPackageArray.packageArray[0])
            else:
                print("LoadRemainingPackages Error")
            

    # Finds the distance between a hub and all the packages in each truck's array.
    # Returns the truck number with the closest hub & less than 16 packages
    def FindTruckWithNearestHub(self, hubMatrix, package):
        minDistance = hubMatrix.findDistance(self.truck1.currentLocation, package.address)
        truckNumber = 2
        if len(self.truck2.packageArray) < 16:
            for loadedPackage in self.truck2.packageArray:
                distance = hubMatrix.findDistance(loadedPackage.address, package.address)
                if distance < minDistance:
                    minDistance = distance
                    truckNumber = 2
        if (len(self.truck3.packageArray) + len(self.truck3.wrongAddressPackages) < 16):
            for loadedPackage in self.truck3.packageArray:
                distance = hubMatrix.findDistance(loadedPackage.address, package.address)
                if distance < minDistance:
                    minDistance = distance
                    truckNumber = 3
        return truckNumber

    # Delivers packages, first updating truck 1 and truck 2 packages to "en route"
    # Next, it checks if there are packages loaded on the trucks
    # It then delivers based on a series of if/elif/else statements
    # While looping, it outputs the hashTable contents if time conditions are met
    def DeliverPackages(self, hubMatrix, time, hashTable):
        for package in self.truck1.packageArray:
            hashTable.LoadPackage(package.ID, 1)
        for package in self.truck2.packageArray:
            hashTable.LoadPackage(package.ID, 2)
        output = False
        while self.truck1.packageArray or self.truck2.packageArray or self.truck3.packageArray:
            if self.truck1.packageArray:
                truck1Projection = self.truck1.totalDistanceTraveled + hubMatrix.findDistance(self.truck1.packageArray[0].address, self.truck1.currentLocation)
                truck2Projection = self.truck2.totalDistanceTraveled + hubMatrix.findDistance(self.truck2.packageArray[0].address, self.truck2.currentLocation)
                # If truck 1 has packages and will deliver before truck 2, deliver from truck 1
                if (truck1Projection < truck2Projection):
                    output = self.truck1.DeliverPackages(hubMatrix, time, hashTable)
                # If truck 1 has packages and will not deliver before truck 2, deliver from truck 2
                else:
                    output = self.truck2.DeliverPackages(hubMatrix, time, hashTable)
            else:
                for package in self.truck3.packageArray:
                    hashTable.LoadPackage(package.ID, 3)
                for package in self.truck3.wrongAddressPackages:
                    hashTable.LoadPackage(package.ID, 3)
                # If truck 1 is back at depot, see if we can fix wrong address
                if self.truck3.wrongAddressPackages and self.truck3.CalculateTime((self.truck1.totalDistanceTraveled / 18) + (self.truck3.totalDistanceTraveled / 18) + time) >= 10.3333:
                    self.truck3.FixWrongAddress(hashTable)
                    self.truck3.OrganizePackagesByRoute(hubMatrix)
                if self.truck2.packageArray:
                    truck3Projection = self.truck3.totalDistanceTraveled + self.truck1.totalDistanceTraveled + hubMatrix.findDistance(self.truck3.packageArray[0].address, self.truck1.currentLocation)
                    truck2Projection = self.truck2.totalDistanceTraveled + hubMatrix.findDistance(self.truck2.packageArray[0].address, self.truck2.currentLocation)
                    # If truck 1 is back at depot and truck 2 will deliver faster than truck 3, deliver from truck 3
                    if (truck2Projection < truck3Projection):
                        output = self.truck2.DeliverPackages(hubMatrix, time, hashTable)
                    # If truck 1 is back at depot and truck 3 will deliver faster than truck 2, deliver from truck 3
                    else:
                        output = self.truck3.DeliverPackages(hubMatrix, (self.truck1.totalDistanceTraveled / 18) + time, hashTable)
                # If truck 1 and 2 are at depot, deliver from truck 3
                else:
                    output = self.truck3.DeliverPackages(hubMatrix, (self.truck1.totalDistanceTraveled / 18) + time, hashTable)
            if(output):
                #self.OutputDistances()
                output = False

    # Outputs the total distances of each truck
    def OutputDistances(self):
        print("Truck 1 Total Distance: " + str(self.truck1.totalDistanceTraveled))
        print("Truck 2 Total Distance: " + str(self.truck2.totalDistanceTraveled))
        print("Truck 3 Total Distance: " + str(self.truck3.totalDistanceTraveled))
        print("")

    # If the trucks deliver all packages before the time triggers, this manually triggers outputs at a certain time
    def CheckDeliveries(self, hashTable):
        if(hashTable.CheckDeliveryStatus(9)):
            self.OutputDistances()
        if(hashTable.CheckDeliveryStatus(10)):
            self.OutputDistances()
        if(hashTable.CheckDeliveryStatus(13)):
            self.OutputDistances()
                    
                    
                
