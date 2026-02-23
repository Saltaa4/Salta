# The Countdown

def countdown(n):
    for x in range(n, -1, -1):
        yield x

n = int(input())
for x in countdown(n):
    print(x)