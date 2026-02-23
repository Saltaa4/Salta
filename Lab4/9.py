# Powers of Two

def powers(n):
    for i in range(n + 1):
        yield 2 ** i

n = int(input())

first = True
for x in powers(n):
    if not first:
        print(" ", end="")
    print(x, end="")
    first = False