class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, length):
        self.length = length

    def area(self):
        return self.length * self.length

n = int(input())
square_obj = Square(n)
print(square_obj.area())































# Создаем родительский класс Shape (L3.5).
# Это базовый шаблон для всех фигур.
class Shape:
    # Метод area в базовом классе возвращает 0, как того требует условие.
    # Название метода 'area' менять нельзя.
    def area(self):
        return 0

# Создаем подкласс Square, который наследует от Shape (L3.6 Inheritance).
# Запись Square(Shape) означает, что Square получает все методы класса Shape.
class Square(Shape):
    
    # Метод __init__ для создания объекта квадрата (L3.5).
    def __init__(self, length):
        # Сохраняем длину стороны в атрибут объекта.
        # Название атрибута 'length' менять нельзя по условию.
        self.length = length

    # Переопределяем метод area (L3.7 Method overriding).
    # Теперь для квадрата метод будет считать площадь по формуле.
    def area(self):
        # Возвращаем длину, возведенную в квадрат (self.length ** 2).
        return self.length * self.length

# Считываем ввод и превращаем его в целое число (L1.7 Type casting).
n = int(input())

# Создаем объект класса Square, передавая ему считанное число n.
# Название 'square_obj' можно заменить на любое свое.
square_obj = Square(n)

# Вызываем метод area у нашего объекта и выводим результат.
print(square_obj.area())