class BankAccount:
    def __init__(self,balance):
        self._balance = balance
    
    @property
    def balance(self):
        return self._balance
    
    def deposit(self,amount):
        if(amount < 0):
            raise ValueError("Deposit a must be positive")
        self._balance += amount

    def withdraw(self,amount):
        if(amount <= 0):
            raise ValueError("withdraw amount must be positive")
        if(amount > self.balance):
            raise ValueError("insufficient amount")
        self._balance -= amount
        
    

account = BankAccount(500)
account.balance = -50
account.deposit(-100)
account.withdraw(10000)
