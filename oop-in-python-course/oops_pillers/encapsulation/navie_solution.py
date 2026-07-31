class BadBankAccount:
  def __init__(self, balance):
    self.balance = balance

account = BadBankAccount(0.0)
account.balance = -1 # Oh dear -- balance should not be allowed to be negative
print(account.balance)

# Why is this bad? The `balance` attribute can be set negative in the __init__ method and can be set directly. Setting a negative balance is not allowed in our banking app.
