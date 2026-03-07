class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, gpa):
        super().__init__(name)
        self.gpa = gpa

    def display(self):
        print(f"Student: {self.name}, GPA: {self.gpa}")

data = input().split()
name_input = data[0]
gpa_input = float(data[1])

student = Student(name_input, gpa_input)
student.display()



















# Создаем базовый (родительский) класс Person (тема L3.5).
class Person:
    # Конструктор принимает имя и сохраняет его в атрибут объекта.
    def __init__(self, name):
        self.name = name

# Создаем дочерний класс Student, который наследует Person (L3.6 Inheritance).
class Student(Person):
    # Конструктор студента принимает два параметра: имя и средний балл (gpa).
    def __init__(self, name, gpa):
        # Функция super() обращается к родительскому классу (Person).
        # Мы вызываем его __init__, чтобы он сам сохранил имя. 
        # Это избавляет нас от дублирования строки self.name = name.
        super().__init__(name)
        # Сохраняем gpa как дополнительный атрибут, уникальный для студента.
        self.gpa = gpa

    # Метод для вывода информации.
    def display(self):
        # Используем f-строку (L1.9) для подстановки имени и балла в текст.
        # Обрати внимание: self.name доступен студенту, так как он унаследовал его.
        print(f"Student: {self.name}, GPA: {self.gpa}")

# Считываем ввод. Разделяем строку по пробелу (L1.8).
# Например, "Aman 3.5" превратится в ["Aman", "3.5"].
data = input().split()

# Имя берем как строку, а балл переводим в число с плавающей точкой float (L1.7).
name_val = data[0]
gpa_val = float(data[1])

# Создаем объект класса Student.
# При этом сработает __init__ класса Student, который внутри вызовет __init__ класса Person.
new_student = Student(name_val, gpa_val)

# Вызываем метод вывода.
new_student.display()