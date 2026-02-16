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
