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

    @staticmethod
    def get_discount(self, cost):
        return (cost * Member._discount_rate) / 100

    @staticmethod
    def set_discount_rate(self, new_discount_rate):
        Member._discount_rate = new_discount_rate

    @staticmethod
    def display_info(self):
        print(f"Member Discount Rate : {Member._discount_rate}%")

#Gold Member
class GoldMember:
    _discount_rate = 12

    def __init__(self, reward_rate = 100):
        self._reward_rate = reward_rate
        self._reward = 0

    @staticmethod
    def get_discount(cost):
        return (cost * GoldMember._discount_rate) / 100

    def set_discount_rate(self, new_discount_rate):
        GoldMember._discount_rate = new_discount_rate

    def set_reward_rate(self, new_reward_rate):
        self._reward_rate = new_reward_rate

    def get_reward(self, rental_cost_after_discount):
        return round(rental_cost_after_discount * self._reward_rate/100)

    def update_reward(self, reward):
        self._reward += reward

    def display_info(self):
        print(f"Discount Rate : {GoldMember._discount_rate} \nReward Rate   : {self._reward_rate} \nReward        : {self._reward}")

#Book
class Book:

    def __init__(self, ID, name, category):
        self._ID = ID
        self._name = name
        self._category = category

    def get_price(self, days):
        return self._category.get_price(days)

    def display_info(self):
        print(f"ID : {self._ID} \nName : {self._name} \nCategory : {self._category}")

    def get_ID(self):
        return self._ID

    def get_name(self):
        return  self._name

    def get_category(self):
        return  self._category

#Book Category
class BookCategory:

    def __int__(self, ID, name, price_1, price_2):
        self._ID = ID
        self._name = name
        self._price_1 = price_1
        self._price_2 = price_2
        self._books = []

    def get_price(self, days):
        return days * (self._price_2 if days >= 10 else self._price_1)

    def add_book(self, book):
        self._books.append(book)

    def display_info(self):
        print(f"CategoryID : {self._ID} \nName : {self._name}\n Price1 : {self._price_1}\n Price2 : {self._price_2}\n Books: {[book.get_name() for book in self._books]}")
