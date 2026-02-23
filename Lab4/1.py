# Squares of Numbers

def square_generator(n):
    for i in range(1, n + 1):
        yield i ** 2

n = int(input())
for square in square_generator(n):
    print(square)