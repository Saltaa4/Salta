class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        pi = 3.14159
        return pi * (self.radius ** 2)

r_value = int(input())
my_circle = Circle(r_value)
result = my_circle.area()
print(f"{result:.2f}")






















# Создаем класс Circle (тема L3.5).
class Circle:
    
    # Метод __init__ (конструктор) срабатывает при создании объекта (L3.5).
    # Он принимает один аргумент — радиус (radius).
    def __init__(self, radius):
        # Сохраняем радиус внутри объекта в атрибут self.radius.
        self.radius = radius

    # Метод для вычисления площади (L3.1 и L3.5).
    def area(self):
        # Объявляем константу пи, как указано в условии задачи.
        pi = 3.14159
        # Считаем площадь по формуле S = pi * r^2.
        # Используем оператор ** для возведения в степень (L1.11).
        circle_area = pi * (self.radius ** 2)
        # Возвращаем полученное число.
        return circle_area

# Считываем ввод пользователя и преобразуем его в целое число (L1.7).
r_value = int(input())

# Создаем объект (экземпляр) класса Circle, передавая ему радиус.
# Название переменной 'my_circle' можно изменить на любое свое.
my_circle = Circle(r_value)

# Вызываем метод area нашего объекта и сохраняем результат в переменную.
result = my_circle.area()

# Выводим результат с помощью f-строки (L1.9).
# Форматирование :.2f округляет число до 2-х знаков после запятой.
print(f"{result:.2f}")