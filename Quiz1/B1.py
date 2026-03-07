a = int(input())
b = int(input())
k = int(input())

count = 0

for i in range(a, b + 1):
    if i % k == 0:
        count += 1

print(count)


# Range and divisibility
# You are given three integers a, b, and k.
# Count how many integers in the interval [a, b] are divisible by k.



def count_divisible(a, b, k):
    count = 0
    for i in range(a, b + 1):
        if i % k == 0:
            count += 1
    return count


a = int(input())
b = int(input())
k = int(input())

print(count_divisible(a, b, k))
