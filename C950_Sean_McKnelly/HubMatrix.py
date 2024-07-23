class HubMatrix:
    def __init__(self):
        # The hub matrix includes all hubs and the distances between hubs
        # once populated.
        self.hubMatrix = []
        # The list of hubs includes a list of all addresses
        self.listOfHubs = ["4001 South 700 East",
                           "1060 Dalton Ave S",
                           "1330 2100 S",
                           "1488 4800 S",
                           "177 W Price Ave",
                           "195 W Oakland Ave",
                           "2010 W 500 S",
                           "2300 Parkway Blvd",
                           "233 Canyon Rd",
                           "2530 S 500 E",
                           "2600 Taylorsville Blvd",
                           "2835 Main St",
                           "300 State St",
                           "3060 Lester St",
                           "3148 S 1100 W",
                           "3365 S 900 W",
                           "3575 W Valley Central Station bus Loop",
                           "3595 Main St",
                           "380 W 2880 S",
                           "410 S State St",
                           "4300 S 1300 E",
                           "4580 S 2300 E",
                           "5025 State St",
                           "5100 South 2700 West",
                           "5383 S 900 East #104",
                           "600 E 900 South",
                           "6351 South 900 East"]
        self.amountOfHubs = len(self.listOfHubs)

    # Populates hub matrix
    def loadHubs(self):
            # Strips all lines from the WGUPUS Distance Table
            # then appends the values in each line to cleanedLines
            with open('Additional Files/WGUPS Distance Table.csv', mode='r') as file:
                allLines = file.readlines()

            cleanedLines = []
            for line in allLines:
                values = line.split(',')
                if len(values) < 27:
                    continue
                
                while(len(values) > 27):
                    values.pop(0)

                cleanedLines.append(values)

            # Populates the hub matrix with the names of all addresses
            # then appends a list of all addresses to each address
            for x in range(len(self.listOfHubs)):
                self.hubMatrix.append([self.listOfHubs[x],[]])
                for y in range(len(self.listOfHubs)):
                    self.hubMatrix[x][1].append([self.listOfHubs[y], 0.0])
        
            # Appends the distance between the hub and each other location
            # (and itself)
            for x in range(27):
                for y in range(27):
                    if cleanedLines[x][y] == "0.0\n":
                        cleanedLines[x][y] = 0.0
                    if y > x:
                        self.hubMatrix[x][1][y][1] = float(cleanedLines[y][x])
                    else:
                        self.hubMatrix[x][1][y][1] = float(cleanedLines[x][y])

    # Checks if a string has any alphabet characters
    def hasLetters(self, stringy):
        return any(char.isalpha() for char in stringy)

    # Prints all the addresses, their linked addresses, and the distances
    # between them.
    def printAll(self):
        for x in range(27):
            print(self.hubMatrix[x][0])
            print("***")
            for y in range(27):
                print(self.hubMatrix[x][1][y][0])
                print(self.hubMatrix[x][1][y][1])
            print("")

    # Returns the distance between two hubs
    def findDistance(self, currentLocation, destination):
        for x in range(self.amountOfHubs):
            if currentLocation in self.hubMatrix[x][0]:
                for y in range(self.amountOfHubs):
                    if destination in self.hubMatrix[x][1][y][0]:
                        return self.hubMatrix[x][1][y][1]

        

