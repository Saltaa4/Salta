class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def total_salary(self):
        return float(self.base_salary)

class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        super().__init__(name, base_salary)
        self.bonus_percent = bonus_percent

    def total_salary(self):
        return self.base_salary * (1 + self.bonus_percent / 100)

class Developer(Employee):
    def __init__(self, name, base_salary, completed_projects):
        super().__init__(name, base_salary)
        self.completed_projects = completed_projects

    def total_salary(self):
        return self.base_salary + (self.completed_projects * 500)

class Intern(Employee):
    def total_salary(self):
        return float(self.base_salary)

data = input().split()
emp_type = data[0]
name = data[1]
base_salary = int(data[2])

if emp_type == "Manager":
    bonus = int(data[3])
    emp = Manager(name, base_salary, bonus)
elif emp_type == "Developer":
    projects = int(data[3])
    emp = Developer(name, base_salary, projects)
else:
    emp = Intern(name, base_salary)

print(f"Name: {emp.name}, Total: {emp.total_salary():.2f}")

























# Базовый класс для всех сотрудников (тема L3.5).
class Employee:
    # Конструктор сохраняет имя и базовую зарплату (L3.5).
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    # Базовый метод расчета зарплаты.
    def total_salary(self):
        return float(self.base_salary)

# Класс Manager наследует Employee (тема L3.6).
class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        # Вызываем конструктор родителя для сохранения общих данных (L3.6 super()).
        super().__init__(name, base_salary)
        self.bonus_percent = bonus_percent

    # Переопределяем метод расчета с учетом процента (L3.7).
    def total_salary(self):
        # Формула: оклад * (1 + процент/100)
        return self.base_salary * (1 + self.bonus_percent / 100)

# Класс Developer наследует Employee.
class Developer(Employee):
    def __init__(self, name, base_salary, completed_projects):
        super().__init__(name, base_salary)
        self.completed_projects = completed_projects

    # Переопределяем метод: к окладу добавляется бонус за проекты.
    def total_salary(self):
        # Формула: оклад + (проекты * 500)
        return self.base_salary + (self.completed_projects * 500)

# Класс Intern наследует Employee.
class Intern(Employee):
    # Интерн получает только базу, поэтому переопределяем метод просто для возврата float.
    def total_salary(self):
        return float(self.base_salary)

# Считываем данные и разбиваем строку в список (L1.8 и L2.3).
data = input().split()
emp_type = data[0]  # Тип сотрудника (Manager, Developer или Intern)
name = data[1]      # Имя
base_salary = int(data[2]) # Оклад

# Выбираем, какой объект создать, используя условия (L1.12).
if emp_type == "Manager":
    bonus = int(data[3])
    emp = Manager(name, base_salary, bonus)
elif emp_type == "Developer":
    projects = int(data[3])
    emp = Developer(name, base_salary, projects)
else:
    # Для интерна дополнительных данных в строке нет.
    emp = Intern(name, base_salary)

# Выводим результат. Нам не важно, какой именно объект в переменной 'emp', 
# у всех есть метод total_salary() и атрибут name.
# .2f форматирует число до двух знаков после запятой (L1.9).
print(f"Name: {emp.name}, Total: {emp.total_salary():.2f}")