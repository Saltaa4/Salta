def isUsual(num: int) -> bool:
    
    while num % 2 == 0:
        num //= 2
    while num % 3 == 0:
        num //= 3
    while num % 5 == 0:
        num //= 5
    
    return num == 1

n = int(input())

if isUsual(n):
    print("Yes")
else:
    print("No")

