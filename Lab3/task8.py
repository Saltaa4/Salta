class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return self.balance
        else:
            return "Insufficient Funds"

data = input().split()
initial_balance = int(data[0])
withdrawal_amount = int(data[1])

my_account = Account("Owner", initial_balance)
print(my_account.withdraw(withdrawal_amount))
