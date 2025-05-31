#Customer
class Customer:
    def __init__(self, ID, name):
        self._ID = ID
        if not name.isalpha():
            raise ValueError("Name is should contain only Alphabets")
        self._name = name

    def getName(self):
        return self._name

    def getID(self):
        return self._ID

    def display_info(self):
        print(f"ID   : { self._ID} \nName : {self._name}")

#Member
class Member:
    _discount_rate = 10 #Discout rate by default for all members

    def get_discount(self, cost):
        return (cost * Member._discount_rate) / 100

    def set_discount_rate(self, new_discout_rate):
        Member._discount_rate = new_discout_rate

    def display_info(self):
        print(f"Member Discout Rate : {Member._discount_rate}%")


