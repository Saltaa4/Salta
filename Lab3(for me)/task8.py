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

























# Создаем класс Account (тема L3.5). 
# Он будет описывать поведение банковского счета.
class Account:
    
    # Метод __init__ создает объект и задает начальные данные (L3.5).
    # Мы принимаем имя владельца (owner) и начальный баланс (balance).
    def __init__(self, owner, balance):
        # Сохраняем значения в атрибуты объекта, чтобы они не потерялись.
        self.owner = owner
        self.balance = balance

    # Метод для пополнения счета.
    def deposit(self, amount):
        # Оператор += прибавляет сумму к текущему балансу (L1.11).
        self.balance += amount

    # Метод для снятия денег.
    def withdraw(self, amount):
        # Проверяем условие: достаточно ли денег на счету (L1.12).
        if amount <= self.balance:
            # Если достаточно, вычитаем сумму из баланса.
            self.balance -= amount
            # Возвращаем обновленный баланс.
            return self.balance
        else:
            # Если денег меньше, чем хотим снять, возвращаем строку с ошибкой.
            # Текст должен быть ровно таким, как в условии задачи.
            return "Insufficient Funds"

# Считываем ввод. Мы получаем строку, например "100 150".
# .split() превращает её в список строк: ["100", "150"] (L1.8).
data = input().split()

# Превращаем строки в целые числа (L1.7 Type casting).
initial_balance = int(data[0])
withdrawal_amount = int(data[1])

# Создаем экземпляр класса. 
# Имя владельца в этой задаче не вводится, поэтому можем написать любое.
my_account = Account("User", initial_balance)

# Вызываем метод withdraw и сразу выводим то, что он вернет (число или строку).
print(my_account.withdraw(withdrawal_amount))