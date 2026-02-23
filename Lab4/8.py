# Prime Numbers Range

def primes(n):
    for x in range(2, n + 1):
        is_prime = True
        for i in range(2, int(x ** 0.5) + 1):
            if x % i == 0:
                is_prime = False
                break
        if is_prime:
            yield x

n = int(input())

first = True
for p in primes(n):
    if not first:
        print(" ", end="")
    print(p, end="")
    first = False