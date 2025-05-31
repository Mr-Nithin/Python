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
class Member(Customer):
    _discount_rate = 10

    def __init__(self, ID, name):
        super().__init__(ID, name)

    @staticmethod
    def get_discount(cost):
        return (cost * Member._discount_rate) / 100

    @staticmethod
    def set_discount_rate(new_discount_rate):
        Member._discount_rate = new_discount_rate


    def display_info(self):
        print(f"ID : {self.getID()} \n Name: {self.getName()}\n Member Discount Rate : {Member._discount_rate}%")



#Gold Member
class GoldMember(Customer):
    _discount_rate = 12

    def __init__(self, ID, name, reward_rate=100):
        super().__init__(ID, name)
        self._reward_rate = reward_rate
        self._reward = 0

    @staticmethod
    def get_discount(cost):
        return (cost * GoldMember._discount_rate) / 100

    @staticmethod
    def set_discount_rate(self, new_discount_rate):
        GoldMember._discount_rate = new_discount_rate

    def set_reward_rate(self, new_reward_rate):
        self._reward_rate = new_reward_rate

    def get_reward(self, rental_cost_after_discount):
        return round(rental_cost_after_discount * self._reward_rate/100)

    def update_reward(self, reward):
        self._reward += reward

    def display_info(self):
        print(f"ID : {self.getID()}\nName : {self.getName()}\nDiscount Rate : {GoldMember._discount_rate}% \nReward Rate   : {self._reward_rate} \nReward        : {self._reward}")

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

    def __init__(self, ID, name, price_1, price_2):
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


#Rental
class Rental:
    def __init__(self, customer, book, days):
        self._customer = customer
        self._book = book
        self._days = days

    def compute_cost(self):
        days = self._days
        book = self._book
        customer = self._customer

        original_cost = book.get_price(days)
        discount = 0
        reward = None

        if hasattr(customer, 'get_discount'):
            discount = customer.get_discount(original_cost)

        total_cost = original_cost - discount

        if hasattr(customer, 'get_reward'):
            reward = customer.get_reward(total_cost)
            return original_cost, discount, total_cost, reward

        return original_cost, discount, total_cost

#Records
class Records:
    def __init__(self):
        self._customers = []
        self._book_categories = []
        self._books = []

    def read_customers(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                customer_type = parts[0].strip()
                customer_id = parts[1].strip()
                customer_name = parts[2].strip()
                discount_rate = parts[3].strip()
                reward_rate = parts[4].strip()
                reward_points = parts[5].strip()
                if customer_type == 'C':
                    customer = Customer(customer_id, customer_name)
                elif customer_type == 'M':
                    customer = Member(customer_id, customer_name)
                    if discount_rate != 'na':
                        Member.set_discount_rate(float(discount_rate) * 100 if float(discount_rate) < 1 else float(discount_rate))
                elif customer_type == 'G':
                    rr = float(reward_rate) * 100 if reward_rate != 'na' and float(reward_rate) < 1 else (float(reward_rate) if reward_rate != 'na' else 100)
                    customer = GoldMember(customer_id, customer_name, rr)
                    if discount_rate != 'na':
                        GoldMember.set_discount_rate(GoldMember, float(discount_rate) * 100 if float(discount_rate) < 1 else float(discount_rate))
                    if reward_points != 'na':
                        customer._reward = int(reward_points)
                else:
                    continue
                self._customers.append(customer)

    def read_books_and_book_categories(self, book_file, category_file):
        book_dict = {}
        with open(book_file, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                book_id = parts[0].strip()
                book_name = parts[1].strip()
                book_dict[book_id] = {'id': book_id, 'name': book_name}
        with open(category_file, 'r') as f:
            for line in f:
                parts = [p.strip() for p in line.strip().split(',')]
                category_id = parts[0]
                category_name = parts[1]
                price_1 = float(parts[2])
                price_2 = float(parts[3])
                book_ids = parts[4:]
                book_category = BookCategory(category_id, category_name, price_1, price_2)
                self._book_categories.append(book_category)
                for book_id in book_ids:
                    if book_id in book_dict:
                        book = Book(book_id, book_dict[book_id]['name'], book_category)
                        self._books.append(book)
                        book_category.add_book(book)

    def find_customer(self, value):
        for customer in self._customers:
            if customer.getID() == value or customer.getName() == value:
                return customer
        return None

    def find_book_category(self, value):
        for book_category in self._book_categories:
            if book_category._ID == value or book_category._name == value:
                return book_category
        return None

    def find_book(self, value):
        for book in self._books:
            if book.get_ID() == value or book.get_name() == value:
                return book
        return None

    def list_customers(self):
        for customer in self._customers:
            customer_id = customer.getID()
            customer_name = customer.getName()
            discount_rate = getattr(customer, '_discount_rate', 'na')
            reward_rate = getattr(customer, '_reward_rate', 'na')
            reward = getattr(customer, '_reward', 'na')
            print(f"ID: {customer_id}, Name: {customer_name}, Discount Rate: {discount_rate}, Reward Rate: {reward_rate}, Reward: {reward}")

    def list_books(self):
        for book in self._books:
            print(f"ID: {book.get_ID()}, Name: {book.get_name()}, Category: {book.get_category().get_name()}")

    def list_book_categories(self):
        for book_category in self._book_categories:
            print(
                f"ID: {book_category.get_ID()}, Name: {book_category.get_name()}, Price 1: {book_category.get_price_1()}, Price 2: {book_category.get_price_2()}, Books: {[book.get_name() for book in book_category.get_books()]}")

