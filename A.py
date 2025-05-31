
import  os
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
        self.customers = []
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
                self.customers.append(customer)

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
        for customer in self.customers:
            if customer.getID() == value or customer.getName() == value:
                return customer
        return None

    def find_book_category(self, value):
        for book_category in self._book_categories:
            if book_category.get_ID  == value or book_category.get_name == value:
                return book_category
        return None

    def find_book(self, value):
        for book in self._books:
            if book.get_ID() == value or book.get_name() == value:
                return book
        return None

    def list_customers(self):
        for customer in self.customers:
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


#Operations

class Operations:
    def __init__(self):
        self._records = Records()
        self._customer_file = 'customers.txt'
        self._book_file = 'books.txt'
        self._category_file = 'book_categories.txt'
        self._files_exist = self._check_files_exist()
        if self._files_exist:
            self._records.read_customers(self._customer_file)
            self._records.read_books_and_book_categories(self._book_file, self._category_file)
        else:
            return

    def _check_files_exist(self):
        missing = []
        for file_name in [self._customer_file, self._book_file, self._category_file]:
            if not os.path.exists(file_name):
                print(f"Error: Required file '{file_name}' is missing.")
                missing.append(file_name)
        if missing:
            print("Exiting program due to missing files.")
            return False
        return True

    def run(self):
        if not self._files_exist:
            return
        while True:
            print("Welcome to the RMIT Book Rental Service!\n")
            print("#################################################################")
            print("You can choose from the following options:")
            print("1: Rent a book")
            print("2: Display existing customers")
            print("3: Display existing book categories")
            print("4: Display existing books")
            print("0: Exit the program")
            print("#################################################################")
            option = input("Choose one Option :  ")
            if option.isdigit():
                option = int(option)
                if 0 <= option <= 4:
                    if option == 1:
                        self._rent_books_session()
                    elif option == 2:
                        self._records.list_customers()
                    elif option == 3:
                        self._records.list_book_categories()
                    elif option == 4:
                        self._records.list_books()
                    elif option == 0:
                        print("Exiting program. Goodbye!")
                        return
                else:
                    print("Please enter a valid option between 0 to 4")
            else:
                print("Enter a valid option a NUMBER between 0 to 4")

    def _rent_books_session(self):
        # Requesting user for Username
        while True:
            customer_name = input("Enter the name of the customer [e.g. Huong]: \n").strip()
            if customer_name.replace(" ", "").isalpha():
                break
            print("It's an invalid name. Please enter a valid single name with alphabets only.")

        customer = self._records.find_customer(customer_name)
        new_customer = False
        if not customer:
            print("Customer not found. Registering new customer.")
            new_id = input("Enter new customer ID: ").strip()
            while True:
                member_type = input("Do you want to be a member? (y/n): ").strip().lower()
                if member_type == 'y':
                    customer = Member(new_id, customer_name)
                    print(f"Registered as Member: {customer_name}")
                    break
                elif member_type == 'n':
                    customer = Customer(new_id, customer_name)
                    print(f"Registered as Customer: {customer_name}")
                    break
                else:
                    print("Please enter 'y' for member or 'n' for just a customer.")
            self._records.customers.append(customer)
            new_customer = True

        rented_books = []
        total_cost = 0
        total_discount = 0
        total_reward = 0

        while True:
            # Requesting user for Book
            while True:
                book_name = input("Enter the book [enter a valid book only, e.g. Harry Potter 1]: \n").strip()
                book = self._records.find_book(book_name)
                if book:
                    break
                else:
                    print("Please enter a valid book name.")

            # Requesting user for number of days
            while True:
                number_of_days_borrowing = input("Enter the number of borrowing days [positive integer only]: \n")
                if number_of_days_borrowing.isdigit():
                    number_of_days_borrowing = int(number_of_days_borrowing)
                    if number_of_days_borrowing > 0:
                        break
                    else:
                        print("Please enter a number greater than 0.")
                else:
                    print("Invalid input. Enter a whole number only.")

            cost_per_day = book.get_category().get_price_1() if number_of_days_borrowing < 10 else book.get_category().get_price_2()
            subtotal = cost_per_day * number_of_days_borrowing
            discount = 0
            reward = 0
            if hasattr(customer, 'get_discount'):
                discount = customer.get_discount(subtotal)
            if isinstance(customer, GoldMember):
                reward = customer.get_reward(subtotal - discount)
                total_reward += reward
            total_cost += subtotal
            total_discount += discount
            rented_books.append((book, number_of_days_borrowing, cost_per_day, reward))

            # Ask if user wants to rent another book
            while True:
                another = input("Would you like to rent another book? (y/n): ").strip().lower()
                if another in ['y', 'n']:
                    break
                else:
                    print("Information is invalid input. Please enter only 'y' for yes or 'n' for no.")
            if another == 'n':
                break

        # Print receipt
        print("------------------------------------------------------------------------------------------")
        print(f"Receipt for {customer.getName()}")
        print("------------------------------------------------------------------------------------------")
        print("Books rented:")
        for book, days, rate, _ in rented_books:
            print(f"  - {book.get_name()} for {days} days ({rate:.2f} AUD/day)")
        print("------------------------------------------------------------------------------------------")
        print(f"Original cost: {total_cost:.2f} (AUD)")
        print(f"Discount: {total_discount:.2f} (AUD)")
        print(f"Total cost: {total_cost - total_discount:.2f} (AUD)")
        if isinstance(customer, GoldMember):
            print(f"Reward: {total_reward}")
        print("Thanks for visiting the library! Have a nice day.")


