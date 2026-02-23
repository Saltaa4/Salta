# Divisibility Check

def gen(n):
    for x in range(0, n + 1, 12):
        yield x

n = int(input())

first = True
for x in gen(n):
    if not first:
        print(' ', end='')
    print(x, end='')
    first = False