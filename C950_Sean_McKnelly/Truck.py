from AllPackagesArray import AllPackagesArray
from Package import Package
from HubMatrix import HubMatrix

class Truck:
    def __init__(self, truckNumber):
        # Truck number
        self.truckNumber = truckNumber
        # Array of packages a truck is holding
        self.packageArray = []
        # Array of packages the truck intends to load
        self.futurePackageArray = []
        # Array including all packages in the truck
        self.totalPackages = []
        # Sets location to WGU, updates later to current location
        self.currentLocation = "4001 South 700 East"
        # The next location the truck intends to drive to
        self.nextLocation = ""
        # Maximum speed of the truck
        self.MPH = 18
        # Total distance traveled by truck
        self.totalDistanceTraveled = 0
        # List of delivered packages, used for checks
        self.deliveredPackageList = []
        # List of packages with wrong address special note
        self.wrongAddressPackages = []
        # List of Grouped Packages
        self.listOfGroupedPackages = [13, 14, 15, 16, 19, 20]

    # Appends a package to packageArray        
    def LoadPackage(self, package):
        self.packageArray.append(package)

    # Appends a package to futurePackageArray
    def FutureLoadPackage(self, package):
        self.futurePackageArray.append(package)

    # Loads mandatory packages to the truck it is mandatory to deliver from
    def LoadMandatoryPackages(self, allPackagesArray):
        index = 0
        while index < len(allPackagesArray.packageArray):
            if ("only be on truck " + str(self.truckNumber)) in allPackagesArray.packageArray[index].GetSpecialNote():
                self.LoadPackage(allPackagesArray.packageArray[index])
                allPackagesArray.packageArray.remove(allPackagesArray.packageArray[index])
                index -= 1
            index += 1

    # Loads grouped packages to packageArray
    def LoadGroupedPackages(self, allPackagesArray):
        index = 0
        while index < len(allPackagesArray.packageArray):
            if int(allPackagesArray.packageArray[index].ID) in self.listOfGroupedPackages:
                self.LoadPackage(allPackagesArray.packageArray[index])
                allPackagesArray.packageArray.remove(allPackagesArray.packageArray[index])
                index -= 1
            index += 1
    
    # "Loads" packages to truck for calculations which are not at the hub yet
    def LoadFuturePackages(self, allPackagesArray):
        index = 0
        while index < len(allPackagesArray.packageArray):
            if "Delayed on flight" in allPackagesArray.packageArray[index].GetSpecialNote():
                self.LoadPackage(allPackagesArray.packageArray[index])
                allPackagesArray.packageArray.remove(allPackagesArray.packageArray[index])
                index -= 1
            elif "Wrong address" in allPackagesArray.packageArray[index].GetSpecialNote():
                self.wrongAddressPackages.append(allPackagesArray.packageArray[index])
                allPackagesArray.packageArray.remove(allPackagesArray.packageArray[index])
                index -= 1
            index += 1

    # Loads an imaginary package, just used for logic to return to WGU
    def LoadImaginaryPackage(self):
         self.LoadPackage(Package(41, "4001 South 700 East", 0, 0, 0, 0, 0, "imaginary package"))

    # Loads packages which have the same address as another package in packageArray
    def LoadPackagesWithSameAddress(self, allPackagesArray):
        # Scans through each package in packageArray
        for package in self.packageArray:
            index = 0
            # Scans through each package in allPackagesArray.packageArray
            # Loads packages that match address
            # Removes the packages that matches from allPackagesArray
            while index < len(allPackagesArray.packageArray):
                if allPackagesArray.packageArray[index].address == package.address:
                    self.LoadPackage(allPackagesArray.packageArray[index])
                    allPackagesArray.packageArray.remove(allPackagesArray.packageArray[index])
                    index -= 1
                index += 1
                
    # Similar to the above method, but only looks at a single package in packageArray
    def LoadPackagesWithSameAddress2(self, allPackagesArray, package):
        index = 0
        while index < len(allPackagesArray.packageArray):
            if allPackagesArray.packageArray[index].address == package.address:
                self.LoadPackage(allPackagesArray.packageArray[index])
                allPackagesArray.packageArray.remove(allPackagesArray.packageArray[index])
                index -= 1
            index += 1

    # Loads a package with 10:30 delivery time
    def LoadEarlyPackage(self, allPackagesArray):
        # Checks to make sure there are packages to be loaded
        if len(allPackagesArray.packageArray) > 0:
            # If a truck is not full and 10:30 is the delivery time, load the package
            if len(self.packageArray) < 16 and "10:30" in allPackagesArray.packageArray[index].deliveryTime:
                self.LoadPackage(allPackageArray.packageArray[0])
                allPackagesArray.packageArray.remove(allPackagesArray.packageArray[0])
                self.LoadPackagesWithSameAddress2(allPackagesArray, self.packageArray[len(self.packageArray) - 1])

    # Organizes the packages on a truck by a fast route that also delivers packages by delivery time                                       
    def OrganizePackagesByRoute(self, hubMatrix, potentialPackages = []):
        self.FixDuplicates()

        totalPackages = self.packageArray + self.futurePackageArray + potentialPackages
        NineAMPackages = []
        TenThirtyAMPackages = []
        EODPackages = []

        # Segments packages by delivery time
        for x in range(len(totalPackages)):
            if totalPackages[x].deliveryTime == "9:00 AM":
                NineAMPackages.append(totalPackages[x])
            elif totalPackages[x].deliveryTime == "10:30 AM":
                TenThirtyAMPackages.append(totalPackages[x])
            elif totalPackages[x].deliveryTime == "EOD":
                EODPackages.append(totalPackages[x])

        # After segmenting packages by zip, organizes packages by distance        
        NineAMPackages = self.SortPackagesByDistance(NineAMPackages, hubMatrix)
        TenThirtyAMPackages = self.SortPackagesByDistance(TenThirtyAMPackages, hubMatrix)
        EODPackages = self.SortPackagesByDistance(EODPackages, hubMatrix)

        # Combines segments in order
        tempPackages = NineAMPackages + TenThirtyAMPackages + EODPackages
        tempPackages2 = []

        # Connects the IDs from the combined segments to the package list, sorts the real package list
        # according to the combined segments
        for x in range(len(tempPackages)):
            for loadedPackage in self.packageArray:
                if str(tempPackages[x][2]) == str(loadedPackage.ID):
                    tempPackages2.append(loadedPackage)
        self.packageArray = tempPackages2

        # Puts the wrong address at the end of the list, to make sure it doesn't get delivered before
        # the address gets corrected
        self.PutWrongAddressLast()

        # This part is to make sure truck 1 returns to WGU before truck 3 begins its route
        if self.truckNumber == 1:
            self.LoadImaginaryPackage()

    def SortPackagesByDistance(self, packageArray, hubMatrix):
        temp = []
        currentLocCopy = self.currentLocation
        index = 0
        # Looks through packageArray and finds the distance between currentLocation and each other package's location,
        # then uses helper sort to sort by [0]-> closest location [1]-> closest location to [0], etc. and returns the output 
        for x in range(len(packageArray)):
            temp.append([packageArray[x].address, hubMatrix.findDistance(self.currentLocation, packageArray[x].address), packageArray[x].ID])
        temp = self.HelperSort(temp, currentLocCopy, hubMatrix)
        return temp

    def HelperSort(self, temp, location, hubMatrix):
        # If the array has more than one value
        if len(temp) > 1:
            # Sort the array by distance from the location we last looked at
            temp = sorted(temp, key=lambda x: x[1])
            # Set the location to the closest location to our current location
            location = temp[0][0]
            # Re-write the distance values from the location we just re-wrote to
            for x in range(len(temp)):
                temp[x][1] = hubMatrix.findDistance(temp[0][0], temp[x][0])
            # Loop through temp
            for x in range(len(temp)):
                # If a value has the same address as the location we set, continue
                if temp[x][1] == 0:
                    continue
                # If not, set the location to the address in temp
                # And recursively call HelperSort
                else:
                    location = temp[x][1]
                    temp = temp[:x] + self.HelperSort(temp[x:], location, hubMatrix)
        # If array has length of one, distance is 0
        elif len(temp) == 1:
            temp[0][1] = 0
        # Return the sorted list
        return temp

    # Calculates distance of a sorted array of package IDs and distances between hubs
    def CalculateDistance(self, temp, hubMatrix):
        distanceTraveled = 0
        if len(temp) > 0:
            for x in range(len(temp)):
                if x == 0:
                    distanceTraveled += hubMatrix.findDistance(self.currentLocation, temp[x][0])
                else:
                    distanceTraveled += hubMatrix.findDistance(temp[x][0], temp[x-1][0])
        return distanceTraveled

    # Takes a starting time and totalDistanceTraveled and determines what time it is
    def CalculateTime(self, time):
        totalTimeTraveled = self.totalDistanceTraveled / self.MPH
        deliveredAt = time + totalTimeTraveled
        return deliveredAt

    # If there is a distance between the currentLocation and the next package's address,
    # finds distance to next location
    # adds that distance to totalDistanceTraveled
    # updates address to next location
    def DriveToLocation(self, hubMatrix):
        if self.packageArray and self.currentLocation != self.packageArray[0].address:
            distanceToLocation = hubMatrix.findDistance(self.currentLocation, self.packageArray[0].address)
            self.totalDistanceTraveled += distanceToLocation
            self.currentLocation = self.packageArray[0].address

    # Delivers a package -- changing status in the hashTable, removing the package from the packageArray,
    # and adding the package to deliveredPackageList

    # Returns output as True if it is time to output the hashTable
    def DeliverPackage(self, hubMatrix, time, hashTable):
        index = 0
        output = False
        while self.packageArray and (index < len(self.packageArray)):
            if self.currentLocation in self.packageArray[index].address:
                if "Wrong address" in self.packageArray[index].specialNote:
                    break
                output = hashTable.DeliverPackage(self.packageArray[index].ID, self.CalculateTime(time), self.truckNumber) or output   
                self.deliveredPackageList.append([self.packageArray[index].ID, self.CalculateTime(time)])
                self.packageArray.remove(self.packageArray[index])
            
            else:
                index += 1
                if index > 16:
                    print("ERROR DeliverPackage(")
                    break
        return output

    # Loads the futurePackageArray into packageArray for truck 3
    def LoadTruck3(self, hubMatrix):
        while self.futurePackageArray:
            self.packageArray.append(self.futurePackageArray[0])
            self.futurePackageArray.remove(self.futurePackageArray[0])
        self.OrganizePackagesByRoute(hubMatrix)

    # Drives to next location and delivers package.
    
    # Outputs True if it is time to output the hashTable
    def DeliverPackages(self, hubMatrix, time, hashTable):
        output = False
        self.DriveToLocation(hubMatrix)
        output = self.DeliverPackage(hubMatrix, time, hashTable)
        return output

    # A simple fix to remove duplicate IDs if a problem arises in the code
    def FixDuplicates(self):
        index = 0
        while index < len(self.packageArray) - 1:
            if self.packageArray[index] in self.packageArray[index + 1:]:
                self.packageArray.remove(self.packageArray[index])
            else:
                index += 1
    
    # Puts the package with the wrong address at the end of the packageArray, so it won't be delivered
    # until it has had time to fix the address
    def PutWrongAddressLast(self):
        for x in range(len(self.packageArray)):
            if "Wrong address" in self.packageArray[x].specialNote:
                temp = self.packageArray[x]
                self.packageArray[x] = self.packageArray[len(self.packageArray) - 1]
                self.packageArray[len(self.packageArray) - 1] = temp

    # Fixes fields both in the hash table and in the packageArray for the wrong address package
    def FixWrongAddress(self, hashTable):
        for package in self.wrongAddressPackages:
            if "Wrong address" in package.specialNote:
                package.address = "410 S State St"
                package.city = "Salt Lake City"
                package.state = "UT"
                package.zipcode = "84111"
                package.specialNote = ""
            hashTable.FixPackageAddress(package.ID, package.address, package.city, package.zipcode)
            self.packageArray.append(package)
            self.wrongAddressPackages.remove(package)
            
                
        
        
            
                
            
        
   
                
            
