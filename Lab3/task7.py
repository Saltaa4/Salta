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
