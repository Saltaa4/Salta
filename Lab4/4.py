# Squares from A to B

def squares(a, b):
    for x in range(a, b + 1):
        yield x * x

a, b = map(int, input().split())
for v in squares(a, b):
    print(v)