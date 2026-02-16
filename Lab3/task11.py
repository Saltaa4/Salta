class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self, other_pair):
        sum_a = self.a + other_pair.a
        sum_b = self.b + other_pair.b
        return sum_a, sum_b

data = input().split()
a1, b1 = int(data[0]), int(data[1])
a2, b2 = int(data[2]), int(data[3])

pair1 = Pair(a1, b1)
pair2 = Pair(a2, b2)

res_a, res_b = pair1.add(pair2)
print(f"Result: {res_a} {res_b}")
