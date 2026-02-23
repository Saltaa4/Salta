# Even Numbers Generator

def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i

n = int(input().strip())

first = True
for num in even_numbers(n):
    if not first:
        print(",", end="")
    print(num, end="")
    first = False