n = int(input())
numbers = list(map(int, input().split()))

max = numbers[0]

for x in numbers:
    if x > max:
        max = x

print(max)
