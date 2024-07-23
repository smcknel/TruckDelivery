from Package import Package

class AllPackagesArray:
    def __init__(self):
        # Creates an empty package array
        self.packageArray = []
        # Strips values from WGUPS Package File, creates a Package object from
        # each line, then appends them to the package array
        with open('Additional Files/WGUPS Package File.csv', mode='r') as file:
            allLines = file.readlines()
        for line in allLines:
            values = line.strip().split(',')
            ID = values[0]
            address = values[1]
            city = values[2]
            state = values[3]
            zipcode = values[4]
            deliveryTime = values[5]
            weight = values[6]
            specialNote = values[7]
            currentPackage = Package(ID, address, city, state, zipcode,
                                     deliveryTime, weight, specialNote)
            self.packageArray.append(currentPackage)

    #prints the special note in packageArray's packages
    def printAll(self):
        for package in self.packageArray:
            print(package.GetSpecialNote())
            
            
            

        
        
