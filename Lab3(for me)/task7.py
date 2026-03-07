class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(f"({self.x}, {self.y})")

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def dist(self, other_point):
        distance = ((self.x - other_point.x)**2 + (self.y - other_point.y)**2)**0.5
        return distance

line1 = input().split()
p1 = Point(int(line1[0]), int(line1[1]))
p1.show()

line2 = input().split()
p1.move(int(line2[0]), int(line2[1]))
p1.show()

line3 = input().split()
p2 = Point(int(line3[0]), int(line3[1]))

result = p1.dist(p2)
print(f"{result:.2f}")























# Создаем класс Point для работы с точками на плоскости (L3.5).
class Point:
    # Метод __init__ инициализирует координаты точки (L3.5).
    def __init__(self, x, y):
        # self.x и self.y — атрибуты, которые хранят положение точки.
        self.x = x
        self.y = y

    # Метод show выводит координаты в нужном формате.
    # Используем f-строку (L1.9) для удобного форматирования.
    def show(self):
        print(f"({self.x}, {self.y})")

    # Метод move меняет текущие координаты на новые.
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    # Метод dist принимает другой объект класса Point (other_point).
    def dist(self, other_point):
        # Вычисляем разность координат по x и y.
        dx = self.x - other_point.x
        dy = self.y - other_point.y
        # Формула: корень из суммы квадратов разностей.
        # ** 2 — это квадрат, ** 0.5 — это корень (L1.11).
        distance = (dx**2 + dy**2)**0.5
        return distance

# Читаем первую строку, разбиваем её и создаем первую точку.
line1 = input().split()
x1, y1 = int(line1[0]), int(line1[1])
p1 = Point(x1, y1)
# Показываем начальные координаты.
p1.show()

# Читаем вторую строку и перемещаем первую точку.
line2 = input().split()
x2, y2 = int(line2[0]), int(line2[1])
p1.move(x2, y2)
# Показываем координаты после перемещения.
p1.show()

# Читаем третью строку и создаем вторую точку для сравнения.
line3 = input().split()
x3, y3 = int(line3[0]), int(line3[1])
p2 = Point(x3, y3)

# Считаем расстояние между перемещенной первой точкой и новой второй точкой.
result = p1.dist(p2)

# Выводим расстояние с двумя знаками после запятой (L1.9).
# .2f указывает Python округлить число до 2-х знаков.
print(f"{result:.2f}")