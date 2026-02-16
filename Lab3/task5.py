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
