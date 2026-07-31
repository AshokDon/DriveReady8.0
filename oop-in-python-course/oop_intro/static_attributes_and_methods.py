
# static attributes and methods

# Let's say that we want to keep track of the total number of user objects that have been created. To do that, we can create a "static" attribute on the User class:



class User:
    total_users_created = 0 #static attribute
    def __init__(self,username,email,password,isAdmin = False):
        self.username = username
        self._email = email # protected 
        self.password = password
        self.isAdmin = isAdmin
        User.total_users_created += 1

    #instance method
    def sayHiToUser(self,user):
        print(f"Sending message to {user.username} : Hi {user.username} , it's {self.username}")

    #instance method
    @property
    def email(self):
        return self._email
    
    #instamnce method
    @email.setter
    def email(self,newemail):
        if('@' in newemail):
            self._email = newemail
        else:
            print("not changed")

    @staticmethod
    def SignUp():
        print("the Signup is Done")

#------------------------------XXXXXXXXXXXXXXXX----------------------------------------
class BankAccount:
    MIN_BALANCE = 100  # Class/static attribute, minimum balance requirement

    def __init__(self, owner, balance=0):
        self.owner = owner  # Instance attribute
        self.balance = balance  # Instance attribute

    # Instance method
    def deposit(self, amount):
        """Add amount to the account balance."""
        if amount > 0:
            self.balance += amount
            print(f"{self.owner}'s new balance: ${self.balance}")
        else:
            print("Deposit amount must be positive.")

    # Static method
    @staticmethod
    def is_valid_interest_rate(rate):
        """Check if the interest rate is within a valid range (0 to 5%)."""
        return 0 <= rate <= 5


# Example usage
account = BankAccount("Alice", 500)

# Using instance method
account.deposit(200)  # Output: Alice's new balance: $700

# Using static method
print(BankAccount.is_valid_interest_rate(3))  # Output: True
print(BankAccount.is_valid_interest_rate(10))  # Output: False

# Example:


class Person:
    def __init__(self, name, email, address) -> None:
        self.name = name  # public attribute
        self._email = email  # protected attribute
        self.__home_address = address  # private attribute

    def print_details(self):
        print(
            f"Name: {self.name}; Email: {self._email}; Address: {self.__home_address}"
        )


person = Person("danny", "danny@gmail.com", "200 Springfield way, UK")
person.print_details()  # Name: danny; Email: danny@gmail.com; Address: 200 Springfield way, UK

print(person.name)  # danny
print(person._email)  # danny@gmail.com (but we are not supposed to do this!)
print(
    person.__home_address
)  # AttributeError: 'Person' object has no attribute '__home_address'
