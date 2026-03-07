class Shape:
    def area(self):
        return 0

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

data = input().split()
l = int(data[0])
w = int(data[1])

rect = Rectangle(l, w)
print(rect.area())






















# Объявляем базовый класс Shape (тема L3.5). 
# Это общая концепция фигуры, у которой площадь по умолчанию 0.
class Shape:
    # Метод area возвращает 0. Название 'area' фиксированное по условию.
    def area(self):
        return 0

# Создаем класс Rectangle. В скобках пишем Shape — это означает наследование (L3.6).
# Теперь Rectangle считается "ребенком" класса Shape и умеет всё то же самое.
class Rectangle(Shape):
    
    # Метод __init__ настраивает наш объект при создании (L3.5).
    # Мы передаем ему два параметра: length (длина) и width (ширина).
    def __init__(self, length, width):
        # self.length и self.width — это атрибуты. Мы сохраняем в них значения,
        # чтобы они были доступны внутри всего объекта.
        self.length = length
        self.width = width

    # Мы создаем свой метод area внутри Rectangle. 
    # Это называется переопределение метода (L3.7 Method overriding).
    # Теперь для прямоугольника будет работать эта формула, а не родительский "return 0".
    def area(self):
        # Площадь прямоугольника — это произведение его сторон.
        return self.length * self.width

# Считываем данные. input() получает строку, например "10 5".
# Метод .split() режет её по пробелу на список: ["10", "5"] (L1.8 и L2.3).
data = input().split()

# Достаем элементы из списка по их индексам и превращаем в целые числа (L1.7).
# data[0] — это первый элемент ("10"), data[1] — второй ("5").
l = int(data[0])
w = int(data[1])

# Создаем экземпляр (объект) класса Rectangle.
# Название переменной 'rect' можно заменить на любое другое.
rect = Rectangle(l, w)

# Вызываем метод area через точку и выводим результат на экран.
print(rect.area())