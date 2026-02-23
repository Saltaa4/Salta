# Limited Cycle

def cycle(lst, k):
    for _ in range(k):
        for x in lst:
            yield x

lst = input().split()
k = int(input())

first = True
for x in cycle(lst, k):
    if not first:
        print(" ", end="")
    print(x, end="")
    first = False