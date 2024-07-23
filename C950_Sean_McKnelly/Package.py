# Simple class for package that includes ID, address, city, state, zipcode,
# intended delivery time, and special note
class Package:
    def __init__(self, ID, address, city, state, zipcode, deliveryTime, weight, specialNote):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deliveryTime = deliveryTime
        self.specialNote = specialNote

    # Returns special note
    def GetSpecialNote(self):
        return self.specialNote
