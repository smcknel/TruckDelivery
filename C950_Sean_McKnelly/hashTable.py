class AllPackagesHashTable:
    def __init__(self):
        # Creates the hash table
        self.table = [[],[],[],[],[],[],[],[],[],[]]
        # Checks are for part D to hold a boolean to see if we still need to
        # do the first, second, and third check
        self.firstOutputCheck = True
        self.secondOutputCheck = True
        self.thirdOutputCheck = True

    def InsertPackage(self, insertID):
        # Checks the WGUPS Package File to see if there's an ID match.
        # If there is a match, adds the package information to the hash table.
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
            if int(insertID) == int(ID):
                hashValue = int(ID) % 10
                self.table[hashValue].append([ID, address, deliveryTime, city, zipcode, weight, ["At the hub", "NA"]])

    # Returns the package's information given an ID
    def LookUp(self, lookUpID):
        hashValue = int(lookUpID) % 10
        for node in self.table[hashValue]:
            if int(lookUpID) == int(node[0]):
                return node[1] + ", " + node[2] + ", " + node[3] + ", " + node[4] + ", " + node[5] + ", " + node[6][0] + ", " + node[6][1]

    # Used to change the wrong address package's values
    def FixPackageAddress(self, ID, address, city, zipcode):
        hashValue = int(ID) % 10
        for node in self.table[hashValue]:
            if str(node[0]) == str(ID):
                node[1] = address
                node[3] = city
                node[4] = zipcode
                node[6][0] = "En Route"
                node[6][1] = "NA"

    # Changes the status of a package from at the hub to "En Route"
    def LoadPackage(self, lookUpID, truckNumber):
        hashValue = int(lookUpID) % 10
        for node in self.table[hashValue]:
            if int(lookUpID) == int(node[0]):
                   node[6][0] = "En Route in truck #" + str(truckNumber)

    # Changes the status of a package to "Delivered" and includes a delivery time
    def DeliverPackage(self, lookUpID, deliveredAt, truckNumber):
        hashValue = int(lookUpID) % 10
        for node in self.table[hashValue]:
            if int(lookUpID) == int(node[0]):
                   node[6][0] = "Delivered by truck #" + str(truckNumber)
                   node[6][1] = self.floatToTime(deliveredAt)
        output = self.CheckDeliveryStatus(deliveredAt)
        return output


    # Can turn a string time into a float
    def timeToFloat(self, deliveredAt):
        if type(deliveredAt) == str:
            keyIndex = deliveredAt.index(":")
            hour = float(deliveredAt[:keyIndex])
            if hour < 11 and "PM" in deliveredAt:
                hour += 12
            elif hour == 12 and "AM" in deliveredAt:
                hour == 24
            minutes = deliveredAt[keyIndex + 1:keyIndex + 3]
            minutes = float(minutes) * 100 / 60
            deliveredAt = hour + minutes * .01
        return deliveredAt

    # Turns a float into a string time
    def floatToTime(self, deliveredAt):
        hours = int(deliveredAt)
        minutes = deliveredAt - hours
        minutes = minutes * 60 / 100
        minutes = str(round(minutes, 2))
        minutes = minutes[2:]
        if len(minutes) == 1:
            minutes += "0"
        if hours < 12:
            return str(hours) + ":" + minutes + "AM"
        elif hours == 12:
            return str(hours) + ":" + minutes + "PM"
        elif hours > 12 and hours < 24:
            return str(hours - 12) + ":" + minutes + "PM"
        else:
            return "PACKAGE DELIVERY LONGER THAN EOD, ERROR IN PROGRAM"
      
    # Checks the delivery status of all packages at a given time
    def CheckDeliveryStatus(self, deliveredAt):
        deliveredAt = self.timeToFloat(deliveredAt)
        if deliveredAt > 8.58333333 and self.firstOutputCheck:
            self.firstOutputCheck = False
            #print("Outputting Hash Table of Packages at: " + str(self.floatToTime(deliveredAt)))
            #self.OutputAllInOrder()
            return True
        elif deliveredAt > 9.5833333 and self.secondOutputCheck:
            self.secondOutputCheck = False
            #print("Outputting Hash Table of Packages at: " + str(self.floatToTime(deliveredAt)))
            #self.OutputAllInOrder()
            return True
        elif deliveredAt > 12.05 and self.thirdOutputCheck:
            self.thirdOutputCheck = False
            #print("Outputting Hash Table of Packages at: " + str(self.floatToTime(deliveredAt)))
            #self.OutputAllInOrder()
            return True
        return False
    

    # Checks the delivery status of all packages at the 3 given times.
    # Will only output a check if the field boolean for the check is True
    def CheckDeliveries(self):
        self.CheckDeliveryStatus(8.6)
        self.CheckDeliveryStatus(10)
        self.CheckDeliveryStatus(12.5)     

    # Outputs header for print statement
    def PrintStatement(self):
        print("******************")
        print("ID (0) / Dest. Address (1) / Required Delivery Time (2) / Dest. City (3)")
        print("Dest. Zipcode (4) / Package Weight (5) / Delivery Status (6) / Delivered At (7)")
        print("******************")
        
    # Outputs all of a hash table's information in the order it is stored
    def OutputAll(self):
        self.PrintStatement()
        for nodes in self.table:
            for node in nodes:
                print(node[0] + " / " + node[1] + " / " + node[2] + " / " + node[3] + " / " )
                print(node[4] + " / " + node[5] + " / " + node[6][0] + " / " + node[6][1])
        print("")
    
    # Outputs all of a hash table's information in the order of IDs
    def OutputAllInOrder(self):
        self.PrintStatement()
        for x in range(41):
            if x == 0:
                continue
            print(str(x) + "," + self.LookUp(x))
        print("")


    
    # Outputs package information at a given time
    def OutputPackage(self, lookUpID, time, trucks):
        address = ""
        city = ""
        zipcode = ""
        reqDeliveryTime = ""
        weight = ""
        deliveredAt = ""
        deliveryStatus = ""
        hashValue = int(lookUpID) % 10
        for node in self.table[hashValue]:
            if int(lookUpID) == int(node[0]):
                if int(lookUpID) == 9 and self.timeToFloat(time) < 10.3333334:
                    address = "300 State St"
                    city = "Salt Lake City"
                    zipcode = "84103"
                else:
                    address = node[1]
                    city = node[3]
                    zipcode = node[4]
                reqDeliveryTime = node[2]
                weight = node[5]
                if self.timeToFloat(time) >= self.timeToFloat(node[6][1]):
                    deliveredAt = node[6][1]
                    deliveryStatus = node[6][0]
                else:
                    if self.timeToFloat(time) <= 8:
                        deliveredAt = "NA"
                        deliveryStatus = "At the hub"
                    elif "truck #3" in node[6][0]:
                        if self.timeToFloat(time) <= (8 + trucks.truck1.totalDistanceTraveled / 18):
                            deliveredAt = "NA"
                            deliveryStatus = "At the hub"
                        elif self.timeToFloat(time) <= (8 + trucks.truck1.totalDistanceTraveled / 18 + trucks.truck3.totalDistanceTraveled / 18):
                            deliveredAt = "NA"
                            deliveryStatus = "En route in truck #3"
                        else:
                            deliveredAt = node[6][1]
                            deliveryStatus = node[6][0]
                    elif "truck #1" in node[6][0]:
                        if self.timeToFloat(time) <= (8 + trucks.truck1.totalDistanceTraveled / 18):
                            deliveredAt = "NA"
                            deliveryStatus = "En route in truck #1"
                    elif "truck #2" in node[6][0]:
                        if self.timeToFloat(time) <= (8 + trucks.truck2.totalDistanceTraveled / 18):
                            deliveredAt = "NA"
                            deliveryStatus = "En route in truck #2"
                print(str(lookUpID) + "," + address + "," + reqDeliveryTime + "," + city + "," + zipcode + "," + weight + "," + deliveryStatus + "," + deliveredAt)
                            
                
        
    # Inputs a package ID (or "all") and a time, and outputs the hash table's information of that ID
    def OutputPackages(self, trucks):
        print("")
        ID = str(input("Give me a package ID to search. If you would like all packages, type All. If you would like to quit, type Quit. "))
        if ID == "Quit":
            return False
        time = input("Give me a time to search for the package(s) in the form hours:minutes AM/PM. ")
        print("")
        print("Outputting Hash Table of Package(s) " + ID + " at: " + time)
        self.PrintStatement()
        if ID == "All":
            for x in range(41):
                if x == 0:
                    continue
                self.OutputPackage(x, time, trucks)   
        else:
            self.OutputPackage(int(ID), time, trucks)
        print("")
        if self.timeToFloat(time) <= 8:
            print("Truck 1 Total Distance: 0")
            print("Truck 2 Total Distance: 0")
            print("Truck 3 Total Distance: 0")
        else:
            if self.timeToFloat(time) > (8 + trucks.truck1.totalDistanceTraveled / 18):
                print("Truck 1 Total Distance: " + str(trucks.truck1.totalDistanceTraveled))
            else:
                print("Truck 1 Total Distance: " + str((self.timeToFloat(time) - 8) * 18))
            if self.timeToFloat(time) > (8 + trucks.truck2.totalDistanceTraveled / 18):
                print("Truck 2 Total Distance: " + str(trucks.truck2.totalDistanceTraveled))
            else:
                print("Truck 2 Total Distance: " + str((self.timeToFloat(time) - 8) * 18))
            if self.timeToFloat(time) <= (8 + trucks.truck1.totalDistanceTraveled / 18):
                print("Truck 3 Total Distance: 0")
            elif self.timeToFloat(time) > (8 + trucks.truck1.totalDistanceTraveled / 18 + trucks.truck3.totalDistanceTraveled / 18):
                print("Truck 3 Total Distance: " + str(trucks.truck3.totalDistanceTraveled))
            else:
                print("Truck 3 Total Distance: " + str((self.timeToFloat(time) - 8) * 18 - trucks.truck1.totalDistanceTraveled))
        return True
                    
                      
                            
                    
            
                
