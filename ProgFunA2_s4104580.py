'''

Name:  Nithin Tharabahalli Manjunath
StudentID : S4104580
Challanges :
There were challenges handling file and simultaneously handling exceptions
There are certain details were I have completely adapted from the Assignment 1
I have covered the most of the scenarios with handling custom exception
I have tried to implement Encapsulation as much as possible.

References:
W3Schools
Python.org

'''

import os
import sys
import datetime

#Customer
class Customer:
    def __init__(self, ID, name):
        self.ID = ID
        if not name.isalpha():
            raise ValueError("Name is should contain only Alphabets")
        self.name = name

    def getName(self):
        return self.name

    def getID(self):
        return self.ID

    def display_info(self):
        print(f"ID   : { self.ID} \nName : {self.name}")


#Member
class Member(Customer):
    discount_rate = 10

    def __init__(self, ID, name):
        super().__init__(ID, name)

    @staticmethod
    def get_discount(cost):
        return (cost * Member.discount_rate) / 100

    @staticmethod
    def set_discount_rate(new_discount_rate):
        Member.discount_rate = new_discount_rate


    def display_info(self):
        print(f"ID : {self.getID()} \n Name: {self.getName()}\n Member Discount Rate : {Member.discount_rate}%")



#Gold Member
class GoldMember(Customer):
    discount_rate = 12

    def __init__(self, ID, name, reward_rate=100):
        super().__init__(ID, name)
        self.reward_rate = reward_rate
        self.reward = 0

    @staticmethod
    def get_discount(cost):
        return (cost * GoldMember.discount_rate) / 100

    @staticmethod
    def set_discount_rate(self, new_discount_rate):
        GoldMember.discount_rate = new_discount_rate

    def set_reward_rate(self, new_reward_rate):
        self.reward_rate = new_reward_rate

    def get_reward(self, rental_cost_after_discount):
        return round(rental_cost_after_discount * self.reward_rate/100)

    def update_reward(self, reward):
        self.reward += reward

    def display_info(self):
        print(f"ID : {self.getID()}\nName : {self.getName()}\nDiscount Rate : {GoldMember.discount_rate}% \nReward Rate   : {self.reward_rate} \nReward        : {self.reward}")

#Book
class Book:

    def __init__(self, ID, name, category):
        self.ID = ID
        self.name = name
        self.category = category

    def get_price(self, days):
        return self.category.get_price(days)

    def display_info(self):
        print(f"ID : {self.ID} \nName : {self.name} \nCategory : {self.category}")

    def get_ID(self):
        return self.ID

    def get_name(self):
        return  self.name

    def get_category(self):
        return  self.category

#Book Category
class BookCategory:

    def __init__(self, ID, name, type, price_1, price_2):
        self.ID = ID
        self.name = name
        self.type = type
        self.price_1 = price_1
        self.price_2 = price_2
        self.books = []

    def get_type(self):
        return self.type

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_price_1(self):
        return self.price_1

    def get_price_2(self):
        return self.price_2

    def get_books(self):
        return self.books

    def get_price(self, days):
        return days * (self.price_2 if days >= 10 else self.price_1)

    def add_book(self, book):
        self.books.append(book)

    def display_info(self):
        print(f"CategoryID : {self.ID} \nName : {self.name}\nType : {self.type}\n Price1 : {self.price_1}\n Price2 : {self.price_2}\n Books: {[book.get_name() for book in self.books]}")


#Rental
class Rental:
    def __init__(self, customer, book, days, timestamp=None):
        self.customer = customer
        self.book = book
        self.days = days
        if timestamp is None:
            self.timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        else:
            self.timestamp = timestamp

    def get_timestamp(self):
        return self.timestamp

    def compute_cost(self):
        days = self.days
        book = self.book
        customer = self.customer

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
        self.book_categories = []
        self.books = []
        self.book_series = []

    def read_customers(self, filename):

        try:
            with open(filename, 'r') as f:
                for line in f:

                    line = line.strip()
                    if not line or line.startswith('#'): continue
                    parts = line.split(',')
                    if len(parts) < 3:
                         continue

                    customer_type = parts[0].strip()
                    customer_id = parts[1].strip()
                    customer_name = parts[2].strip()
                    discount_rate_str = parts[3].strip() if len(parts) > 3 else 'na'
                    reward_rate_str = parts[4].strip() if len(parts) > 4 else 'na'
                    reward_points_str = parts[5].strip() if len(parts) > 5 else 'na'

                    customer = None
                    try:
                        if customer_type == 'C':
                            customer = Customer(customer_id, customer_name)
                        elif customer_type == 'M':
                            customer = Member(customer_id, customer_name)
                            if discount_rate_str != 'na':
                                discount_rate = float(discount_rate_str)
                                Member.set_discount_rate(discount_rate * 100 if discount_rate < 1 else discount_rate)

                        elif customer_type == 'G':
                            initial_reward_rate = 100.0
                            if reward_rate_str != 'na':
                                rr = float(reward_rate_str)
                                initial_reward_rate = rr * 100 if rr < 1 else rr
                            customer = GoldMember(customer_id, customer_name, initial_reward_rate)

                            if discount_rate_str != 'na':
                                discount_rate = float(discount_rate_str)
                                GoldMember.set_discount_rate(GoldMember, discount_rate * 100 if discount_rate < 1 else discount_rate)

                            if reward_points_str != 'na':
                                try:
                                    customer.reward = int(float(reward_points_str))
                                except ValueError:
                                     print(f"Invalid reward score format '{reward_points_str}' for customer {customer_name}")
                                     customer.reward = 0
                        else:
                            continue
                        if customer and self.find_customer(customer.getID()):
                             print(f"Duplicate_customer_ID {customer.getID()} found in {filename}. Ignoring: {line}")
                        elif customer:
                            self.customers.append(customer)
                    except ValueError as ve:
                        raise ve
                    except Exception as ex:
                        raise ex

            print(f"Successfully read customer data from {filename}.")
            # for c in self.customers:
            #     print(f"[DEBUG] Loaded Customer: Type: {type(c).__name__}, Name: {c.getName()}, ID: {c.getID()}") # DEBUG PRINT

        except FileNotFoundError:
            print(f" Customer file '{filename}' not found.")
            raise
        except Exception as e:
            print(f"Something Wrong {filename}: {e}")
            raise

    def read_books_and_book_categories(self, book_file, category_file):
        books_by_id_from_file = {}
        self.books = []
        self.book_series = []
        self.book_categories = []
        try:
            with open(book_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'): continue
                    parts = line.split(',')
                    if len(parts) < 2: continue
                    book_id = parts[0].strip()
                    book_name = parts[1].strip()
                    if not book_id or not book_name: continue
                    if book_id in books_by_id_from_file:
                        print(f"Warning: Duplicate book ID '{book_id}' in {book_file}. Skipping line: {line}")
                        continue
                    book = Book(book_id, book_name, None)
                    books_by_id_from_file[book_id] = book
                    self.books.append(book)


        except FileNotFoundError:
            print(f"Book file '{book_file}' not found.")
        except Exception as e:
            print(f"Something wrong while reading a file {book_file}: {e}")

        try:
            with open(category_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'): continue
                    parts = [p.strip() for p in line.split(',')]

                    if len(parts) < 5: continue

                    category_id = parts[0]
                    category_name = parts[1]
                    category_type = parts[2]
                    price_1_str = parts[3]
                    price_2_str = parts[4]
                    book_names_in_category = parts[5:]

                    if not category_id or not category_name or not category_type or not price_1_str or not price_2_str:
                         print(f"Warning: Skipping invalid category data in {category_file}: {line} (Missing required fields).")
                         continue

                    try:
                        price_1 = float(price_1_str)
                        price_2 = float(price_2_str)

                        if self.find_book_category(category_id):
                             print(f"Warning: Duplicate category ID '{category_id}' in {category_file}. Skipping line: {line}")
                             continue

                        book_category = BookCategory(category_id, category_name, category_type, price_1, price_2)
                        for book_name in book_names_in_category:
                             if not book_name: continue
                             found_book = next((book for book in self.books if book.get_name() == book_name), None)

                             if found_book:
                                 found_book.category = book_category
                                 book_category.add_book(found_book)
                             else:
                                 found_series = next((series for series in self.book_series if series.get_name() == book_name), None)
                                 if found_series:
                                      book_category.add_book(found_series)
                        self.book_categories.append(book_category)

                    except ValueError as ve:
                        pass
                    except Exception as ex:
                         pass


        except FileNotFoundError:
            print(f"Error: Book category file '{category_file}' not found.")
            raise
        except Exception as e:
            print(f"An error occurred while reading book category data from {category_file}: {e}")
            raise

    def find_customer(self, value):
        for customer in self.customers:
            if customer.getID() == value or customer.getName().lower() == value.lower():
                return customer
        return None

    def find_book_category(self, value):
        for book_category in self.book_categories:
            if book_category.ID == value or book_category.name.lower() == value.lower():
                return book_category
        return None

    def find_book(self, value):
        for book in self.books + self.book_series:
            if book.get_ID() == value:
                return book
        for book in self.books + self.book_series:
             if book.get_name().lower() == value.lower():
                 return book
        return None

    def list_customers(self):
        if not self.customers:
            print("\nNo customers to display.\n")
            return
        print("\n### Customer List ###")
        for customer in self.customers:
            customer.display_info()
            print("--------------------")

    def list_books(self):
        if not self.books and not self.book_series:
            print("\nNo books or series to display.\n")
            return
        print("\n### Books-List ###")
        if self.books:
            print("Individual-Books:")
            for book in self.books:
                book.display_info()
                book.get_name()
                print("--")
        if self.book_series:
             print("\nBook-Series:")
             for series in self.book_series:
                  series.display_info()
                  print("--")
        print("--------------------")


    def list_book_categories(self):
        if not self.book_categories:
            print("\nNo book categories to display.\n")
            return
        print("\n### Book Category List ###")
        for book_category in self.book_categories:
            book_category.display_info()
            print("--------------------")


#Operations class
class Operations:
    def __init__(self):
        # Command line argument support
        args = sys.argv[1:] if hasattr(sys, 'argv') else []
        if len(args) == 0:
            self.customer_file = 'customers.txt'
            self.book_file = 'books.txt'
            self.category_file = 'book_categories.txt'
        elif len(args) == 3:
            self.customer_file = args[0]
            self.book_file = args[1]
            self.category_file = args[2]
        else:
            print("Usage: python <program.py> [customer_file book_file book_category_file]")
            sys.exit(1)
        self.records = Records()
        self.files_exist = self._check_files_exist()
        if self.files_exist:
            self.records.read_customers(self.customer_file)
            self.records.read_books_and_book_categories(self.book_file, self.category_file)
        else:
            return

    def _check_files_exist(self):
        missing = []
        for fname in [self.customer_file, self.book_file, self.category_file]:
            if not os.path.exists(fname):
                print(f"Error: Required file '{fname}' is missing.")
                missing.append(fname)
        if missing:
            print("Exiting program due to missing files.")
            return False
        return True

    def run(self):
        if not self.files_exist:
            return
        while True:
            print("Welcome to the RMIT Book Rental Service!\n")
            print("#################################################################")
            print("You can choose from the following options:")
            print("1: Rent a book")
            print("2: Display existing customers")
            print("3: Display existing book categories")
            print("4: Display existing books")
            print("5: Update information of a book category")
            print("6: Update books of a book category")
            print("7: Adjust the discount rate of all members")
            print("8: Adjust the reward rate of a Gold member")
            print("9: Rent books via a file")
            print("10: Display all rentals")
            print("11: Display the most valuable customer")
            print("12: Display a customer rental history")
            print("0: Exit the program")
            print("#################################################################")
            option = input("Choose one Option :  ")
            if option.isdigit():
                option = int(option)
                if 0 <= option <= 12:
                    if option == 1:
                        self._rent_books_session()
                    elif option == 2:
                        self.records.list_customers()
                    elif option == 3:
                        self.records.list_book_categories()
                    elif option == 4:
                        self.records.list_books()
                    elif option == 5:
                        self._update_book_category_info()
                    elif option == 6:
                        self._update_books_of_category()
                    elif option == 7:
                        self._adjust_discount_rate_all_members()
                    elif option == 8:
                        self._adjust_reward_rate_gold_member()
                    elif option == 9:
                        self._rent_books_via_file()
                    elif option == 10:
                        self._display_all_rentals()
                    elif option == 11:
                        self._display_most_valuable_customer()
                    elif option == 12:
                        self._display_customer_rental_history()
                    elif option == 0:
                        self._save_all_data()
                        print("Exiting program. Goodbye!")
                        return
                else:
                    print("Please enter a valid option between 0 to 12")
            else:
                print("Enter a valid option a NUMBER between 0 to 12")

    def _rent_books_session(self):
        # Requesting user for Username
        while True:
            try:
                customer_name = input("Enter the name of the customer [e.g. Huong]: \n").strip()
                if not customer_name.replace(" ", "").isalpha():
                    raise InvalidCustomerNameException("It's an invalid name. Please enter a valid single name with alphabets only.")
                break
            except InvalidCustomerNameException as e:
                print(e)

        customer = self.records.find_customer(customer_name)
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
            self.records.customers.append(customer)
            new_customer = True

        rented_books = []
        total_cost = 0
        total_discount = 0
        total_reward = 0

        while True:

            while True:
                try:
                    book_name = input("Enter the book or book series [enter a valid book or series only, e.g. Harry Potter 1 or S1]: \n").strip()
                    book = self.records.find_book(book_name)
                    if not book:
                        print("Please enter a valid book or book series name/ID.")
                        continue
                    if not isinstance(book, BookSeries):

                        if book.get_category() is None:
                            print(f"Book '{book.get_name()}' does not have a category assigned and cannot be rented.")


                        if book.get_category().get_type().lower() == 'reference':
                             print("This book belongs to a Reference category and cannot be rented. Please choose another book.")
                             continue
                    else:
                         all_components_rentable = True
                         for component_book in book.get_books():
                              if component_book.get_category() is None:
                                   print(f"Book series '{book.get_name()}' cannot be rented because component book '{component_book.get_name()}' does not have a category assigned.")
                                   all_components_rentable = False
                                   break
                              if component_book.get_category().get_type().lower() == 'reference':
                                   print(f"Book series '{book.get_name()}' cannot be rented because component book '{component_book.get_name()}' belongs to a Reference category.")
                                   all_components_rentable = False
                                   break
                         if not all_components_rentable:
                              continue

                    break

                except InvalidBookException as e:
                    print(e)


            while True:
                try:
                    number_of_days_borrowing = input("Enter the number of borrowing days [positive integer only]: \n")
                    if not number_of_days_borrowing.isdigit():
                        raise InvalidBorrowingDaysException("Invalid input. Enter a whole number only.")
                    number_of_days_borrowing = int(number_of_days_borrowing)
                    if number_of_days_borrowing <= 0:
                        raise InvalidBorrowingDaysException("Please enter a number greater than 0.")
                    if not isinstance(book, BookSeries) and book.get_category() is not None and book.get_category().get_type().lower() == 'reference' and number_of_days_borrowing > 14:
                         raise ReferenceBookBorrowDaysException("This book can't be borrowed for more than 14 days. Please enter a valid number of days.")
                    break
                except (InvalidBorrowingDaysException, ReferenceBookBorrowDaysException) as e:
                    print(e)

            if not isinstance(book, BookSeries) and book.get_category() is None:
                 print(f"Skipping rental for book '{book.get_name()}' due to missing category information.")
                 while True:
                      another = input("Would you like to rent another book? (y/n): ").strip().lower()
                      if another in ['y', 'n']:
                           break
                      else:
                           print("Information is invalid input. Please enter only 'y' for yes or 'n' for no.")
                 if another == 'n':
                      break
                 else:
                      continue

            if isinstance(book, BookSeries):
                cost_per_day = book.get_price(1)
                subtotal = cost_per_day * number_of_days_borrowing
            else:
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


            while True:
                another = input("Would you like to rent another book? (y/n): ").strip().lower()
                if another in ['y', 'n']:
                    break
                else:
                    print("Information is invalid input. Please enter only 'y' for yes or 'n' for no.")
            if another == 'n':
                break


        if not hasattr(self, '_rentals'):
            self._rentals = []
        rental_timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        for book, days, _, _ in rented_books:
            rental = Rental(customer, book, days, rental_timestamp)
            self._rentals.append(rental)


        reward_deduction = 0
        reward_points_used = 0
        if isinstance(customer, GoldMember) and customer.reward >= 20:
            max_deduct = customer.reward // 20
            print(f"You have {customer.reward} reward points. You can deduct up to {max_deduct} AUD from your total cost.")
            while True:
                try:
                    use_points = input(f"Would you like to use your reward points to reduce your bill? (y/n): ").strip().lower()
                    if use_points not in ['y', 'n']:
                        print("Please enter only 'y' or 'n'.")
                        continue
                    if use_points == 'y':
                        reward_deduction = max_deduct
                        reward_points_used = reward_deduction * 20
                        break
                    else:
                        break
                except Exception as e:
                    print(e)

        print("------------------------------------------------------------------------------------------")
        print(f"Receipt for {customer.getName()}")
        print(f"Rental timestamp: {rental_timestamp}")
        print("------------------------------------------------------------------------------------------")
        print("Books rented:")
        for book, days, rate, _ in rented_books:
            if isinstance(book, BookSeries):
                print(f"  - Series: {book.get_name()} (ID: {book.get_ID()}) for {days} days ({rate:.2f} AUD/day), Books: {[b.get_name() for b in book.get_books()]}")
            else:
                print(f"  - {book.get_name()} for {days} days ({rate:.2f} AUD/day)")
        print("------------------------------------------------------------------------------------------")

        print(f"{'Original cost:':<35}{total_cost:>10.2f} (AUD)")
        print(f"{'Discount:':<35}{total_discount:>10.2f} (AUD)")
        print(f"{'Total cost:':<35}{(total_cost - total_discount):>10.2f} (AUD)")

        if reward_deduction > 0:
            print(f"{'Reward points used:':<35}{reward_points_used:>10} (-{reward_deduction:>8.2f} AUD)")
            print(
                f"{'Total cost after reward deduction:':<35}{(total_cost - total_discount - reward_deduction):>10.2f} (AUD)")

        if isinstance(customer, GoldMember):
            print(f"{'Reward:':<35}{total_reward:>10}")
            customer.reward = customer.reward - reward_points_used + total_reward
            print(f"{'Current reward points:':<35}{customer.reward:>10}")

        print("Thanks for visiting the library! Have a nice day.")

    def _update_book_category_info(self):

        while True:
            cat_value = input("Enter the book category name or ID to update: ").strip()
            book_category = self.records.find_book_category(cat_value)
            if not book_category:
                print("Book category not found. Please try again.")
                continue
            break

        while True:
            new_type = input("Enter new type (Rental/Reference): ").strip().capitalize()
            if new_type not in ['Rental', 'Reference']:
                print("Invalid type. Please enter 'Rental' or 'Reference'.")
                continue
            break

        while True:
            new_price_1 = input("Enter new price 1 (per day, for <10 days): ").strip()
            try:
                new_price_1 = float(new_price_1)
                if new_price_1 <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid price. Please enter a positive number.")

        while True:
            new_price_2 = input("Enter new price 2 (per day, for >=10 days): ").strip()
            try:
                new_price_2 = float(new_price_2)
                if new_price_2 <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid price. Please enter a positive number.")
        book_category.type = new_type
        book_category.price_1 = new_price_1
        book_category.price_2 = new_price_2
        print(f"Book category '{book_category.get_name()}' updated successfully.")

    def _update_books_of_category(self):
        while True:
            cat_value = input("Enter the book category name or ID to update books: ").strip()
            book_category = self.records.find_book_category(cat_value)
            if not book_category:
                print("Book category not found. Please try again.")
                continue
            break
        print(f"Current books: {[book.get_name() for book in book_category.books]}")
        action = input("Do you want to add or remove books? (add/remove): ").strip().lower()
        if action not in ['add', 'remove']:
            print("Invalid action. Please enter 'add' or 'remove'.")
            return
        book_ids = input("Enter the book or book series to {} (comma separated, by name or ID): ".format(action)).split(',')
        book_ids = [b.strip() for b in book_ids if b.strip()]
        if action == 'add':
            for b in book_ids:
                book = self.records.find_book(b)
                if not book:
                    print(f"Book or series '{b}' not found. Skipping.")
                    continue
                if book in book_category.books:
                    print(f"'{book.get_name()}' is already in the category.")
                    continue
                book_category.books.append(book)
                if hasattr(self.records, 'books') and isinstance(book, Book):
                    if book not in self.records.books:
                        self.records.books.append(book)
                if hasattr(self.records, 'book_series') and isinstance(book, BookSeries):
                    if book not in self.records.book_series:
                        self.records.book_series.append(book)
            print("Books added successfully.")
        elif action == 'remove':
            to_remove = []
            for b in book_ids:
                book = self.records.find_book(b)
                if not book or book not in book_category.books:
                    print(f"Book or series '{b}' not found in this category. Skipping.")
                    continue
                to_remove.append(book)
            for book in to_remove:
                book_category.books.remove(book)
                if hasattr(self.records, 'books') and isinstance(book, Book):
                    if book in self.records.books:
                        self.records.books.remove(book)
                if hasattr(self.records, 'book_series') and isinstance(book, BookSeries):
                    if book in self.records.book_series:
                        self.records.book_series.remove(book)
            print("Books removed successfully.")

    def _adjust_discount_rate_all_members(self):
        while True:
            rate = input("Enter new discount rate for all members (e.g., 0.2 for 20%): ").strip()
            try:
                rate = float(rate)
                if rate <= 0:
                    raise ValueError
                if rate < 1:
                    rate = rate * 100
                Member.set_discount_rate(rate)
                GoldMember.set_discount_rate(GoldMember, rate)
                print(f"Discount rate for all members set to {rate}%.")
                break
            except ValueError:
                print("Invalid rate. Please enter a positive number.")

    def _adjust_reward_rate_gold_member(self):
        while True:
            cust_value = input("Enter the Gold member's name or ID: ").strip()
            customer = self.records.find_customer(cust_value)
            if not customer or not isinstance(customer, GoldMember):
                print("Customer not found or is not a Gold member. Please try again.")
                continue
            break
        while True:
            rate = input("Enter new reward rate (e.g., 1 for 100%): ").strip()
            try:
                rate = float(rate)
                if rate <= 0:
                    raise ValueError
                customer.set_reward_rate(rate * 100 if rate < 1 else rate)
                print(f"Reward rate for Gold member '{customer.getName()}' set to {rate if rate >= 1 else rate * 100}%.")
                break
            except ValueError:
                print("Invalid rate. Please enter a positive number.")

    def _rent_books_via_file(self):
        filename = input("Enter the rental file name: ").strip()
        try:
            with open(filename, 'r') as f:
                for line in f:
                    parts = [p.strip() for p in line.strip().split(',')]
                    if not parts or len(parts) < 6:
                        continue
                    cust_value = parts[0]
                    customer = self.records.find_customer(cust_value)
                    if not customer:
                        print(f"Customer '{cust_value}' not found. Skipping.")
                        continue
                    books_and_days = parts[1:-5]
                    books = books_and_days[::2]
                    days = books_and_days[1::2]
                    for b, d in zip(books, days):
                        book = self.records.find_book(b)
                        if not book:
                            print(f"Book or series '{b}' not found. Skipping.")
                            continue
                        try:
                            d = int(d)
                        except ValueError:
                            print(f"Invalid days '{d}' for book '{b}'. Skipping.")
                            continue
                        rental = Rental(customer, book, d, parts[-1])
                        if not hasattr(self, '_rentals'):
                            self._rentals = []
                        self._rentals.append(rental)
                    # Update GoldMember reward points
                    if isinstance(customer, GoldMember):
                        earned_rewards = int(float(parts[-2]))
                        customer.reward += earned_rewards
            print("Rental file processed successfully.")
        except FileNotFoundError:
            print("Cannot find the rental file.")

    def _display_all_rentals(self):
        if not hasattr(self, '_rentals') or not self._rentals:
            print("No rentals to display.")
            return
        for rental in self._rentals:
            customer = rental.customer
            book = rental.book
            days = rental.days
            timestamp = rental.get_timestamp()
            original_cost = book.get_price(days) if not isinstance(book, BookSeries) else book.get_price(days)
            discount = 0
            if hasattr(customer, 'get_discount'):
                discount = customer.get_discount(original_cost)
            total_cost = original_cost - discount
            reward = None
            if isinstance(customer, GoldMember):
                reward = customer.get_reward(total_cost)
            print("------------------------------")
            print(f"Customer: {customer.getName()} | Book/Series: {book.get_name()} | Days: {days}")
            print(f"Original cost: {original_cost:.2f} | Discount: {discount:.2f} | Total cost: {total_cost:.2f}")
            if reward is not None:
                print(f"Earned rewards: {reward}")
            print(f"Rental time: {timestamp}")
        print("------------------------------")

    def _display_most_valuable_customer(self):
        if not hasattr(self, '_rentals') or not self._rentals:
            print("No rentals to analyze.")
            return
        spend_dict = {}
        for rental in self._rentals:
            customer = rental.customer
            book = rental.book
            days = rental.days
            original_cost = book.get_price(days) if not isinstance(book, BookSeries) else book.get_price(days)
            discount = 0
            if hasattr(customer, 'get_discount'):
                discount = customer.get_discount(original_cost)
            total_cost = original_cost - discount
            spend_dict[customer] = spend_dict.get(customer, 0) + total_cost
        if not spend_dict:
            print("No customer data available.")
            return
        most_valuable = max(spend_dict.items(), key=lambda x: x[1])
        customer, amount = most_valuable
        print(f"Most valuable customer: {customer.getName()} (ID: {customer.getID()})")
        print(f"Total money spent: {amount:.2f} AUD")

    def _display_customer_rental_history(self):
        cust_value = input("Enter the customer's name or ID: ").strip()
        customer = self.records.find_customer(cust_value)
        if not customer:
            print("Customer not found.")
            return
        if not hasattr(self, '_rentals') or not self._rentals:
            print("No rentals to display.")
            return

        customer_rentals = [r for r in self._rentals if r.customer == customer]
        if not customer_rentals:
            print(f"No rental history for {customer.getName()}.")
            return
        print(f"Rental history for {customer.getName()}:")
        print(f"{'Rental':<8} {'Books & Borrowing days':<40} {'Original Cost':<13} {'Discount':<9} {'Final Cost':<10} {'Rewards':<7}")
        for idx, rental in enumerate(customer_rentals, 1):
            session_rentals = [r for r in customer_rentals if r.get_timestamp() == rental.get_timestamp()]

            if session_rentals[0] != rental:
                continue
            books_days = ', '.join([f"{r.book.get_name()}: {r.days} days" for r in session_rentals])
            original_cost = sum(r.book.get_price(r.days) for r in session_rentals)
            discount = sum(customer.get_discount(r.book.get_price(r.days)) if hasattr(customer, 'get_discount') else 0 for r in session_rentals)
            final_cost = original_cost - discount
            rewards = 'na'

            if isinstance(customer, GoldMember):
                rewards = sum(customer.get_reward(r.book.get_price(r.days) - (customer.get_discount(r.book.get_price(r.days)) if hasattr(customer, 'get_discount') else 0)) for r in session_rentals)
            print(f"{idx:<8} {books_days:<40} {original_cost:<13.2f} {discount:<9.2f} {final_cost:<10.2f} {rewards:<7}")

    def _save_all_data(self):
        # Save customers
        with open(self.customer_file, 'w') as f:
            for c in self.records.customers:
                if isinstance(c, GoldMember):
                    f.write(f"G,{c.getID()},{c.getName()},{getattr(c, 'discount_rate', 'na')},{getattr(c, 'reward_rate', 'na')},{getattr(c, 'reward', 'na')}\n")
                elif isinstance(c, Member):
                    f.write(f"M,{c.getID()},{c.getName()},{getattr(c, 'discount_rate', 'na')},na,na\n")
                else:
                    f.write(f"C,{c.getID()},{c.getName()},na,na,na\n")
        # Save books
        with open(self.book_file, 'w') as f:
            for b in self.records.books:
                f.write(f"{b.get_ID()},{b.get_name()}\n")
            for s in getattr(self.records, '_book_series', []):
                f.write(f"{s.get_ID()},{s.get_name()},{','.join([book.get_name() for book in s.get_books()])}\n")
        # Save book categories
        with open(self.category_file, 'w') as f:
            for cat in self.records.book_categories:
                f.write(f"{cat.get_ID()},{cat.get_name()},{cat.get_type()},{cat.get_price_1()},{cat.get_price_2()}{',' if cat.books else ''}{','.join([book.get_ID() for book in cat.books])}\n")
        # Save rentals
        if hasattr(self, '_rentals'):
            with open('rentals.txt', 'w') as f:
                for rental in self._rentals:
                    customer = rental.customer
                    book = rental.book
                    days = rental.days
                    original_cost = book.get_price(days)
                    discount = customer.get_discount(original_cost) if hasattr(customer, 'get_discount') else 0
                    total_cost = original_cost - discount
                    rewards = 'na'
                    if isinstance(customer, GoldMember):
                        rewards = customer.get_reward(total_cost)

# Custom Exceptions
class InvalidCustomerNameException(Exception):
    pass

class InvalidBookException(Exception):
    pass

class InvalidBorrowingDaysException(Exception):
    pass

class ReferenceBookBorrowDaysException(Exception):
    pass

# BookSeries class definition
class BookSeries:
    def __init__(self, ID, name, category, books):
        self.ID = ID
        self.name = name
        self.category = category
        self.books = books  # list of Book objects

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_books(self):
        return self.books

    def get_price(self, days):
        total = sum(book.get_price(days) for book in self.books)
        return 0.5 * total

    def display_info(self):
        print(f"Series ID: {self.ID}\nName: {self.name}\nCategory: {self.category.get_name()}\nComponent Books: {[book.get_name() for book in self.books]}")
        
op = Operations()
op.run()
